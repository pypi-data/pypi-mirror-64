from __future__ import print_function
from __future__ import division

import json
import re
from datetime import datetime

import tensorflow as tf
import google.protobuf.json_format as json_format

CTX_FEATURE_NAMES = ['ppcVisitor', 'sfmcld']

SEQ_FEATURE_NAMES = (
    'timestamp,productpage,search,homepage,event_search,event_pageview,event_imgClick,'
    'event_filterDurationRange,event_productDefaultFilter,event_selectFilter,event_filterAirport,'
    'event_filterDepartureDate,event_imgFeed,event_filterMealplan,event_selectPriceAndDate,'
    'event_partyCompositionFilter,event_flightSelection,event_deleteFilter,'
    'event_selectFlightFilter,event_packageAvailability,event_searchEvent,'
    'event_productAvailability,event_mealPlanSelection,event_roomTypeSelection,'
    'event_selectDurationDay,event_searchWizardShowPopup,event_searchWizardClose,'
    'event_roomTypeDetails,event_contentNavigation,event_showTop10,event_newsletterSub,'
    'event_userID,event_other,sorted_by_None,sorted_by_popularity,sorted_by_dateAscending,'
    'sorted_by_priceAscending,sorted_by_zooverRatingDescending,sorted_by_priceDescending,'
    'sorted_by_hotelRating,sorted_by_price,price_increment').split(',')

EVENT_TRIGGER_CATEGORIES = (
    'search,pageview,imgClick,filterDurationRange,productDefaultFilter,selectFilter,'
    'filterAirport,filterDepartureDate,imgFeed,filterMealplan,'
    'selectPriceAndDate,partyCompositionFilter,flightSelection,'
    'deleteFilter,selectFlightFilter,packageAvailability,searchEvent,productAvailability,'
    'mealPlanSelection,roomTypeSelection,selectDurationDay,'
    'searchWizardShowPopup,searchWizardClose,roomTypeDetails,contentNavigation,'
    'showTop10,newsletterSub,userID,ppcVisitor,sfmcld').split(',')

PAGE_TYPE_CATEGORIES = "productpage,search,homepage".split(',')

SORTED_BY_CATEGORIES = ('None,popularity,dateAscending,priceAscending,zooverRatingDescending,'
                        'priceDescending,hotelRating,price').split(',')

# to-be-filtered out source IP addresses
EXCLUDED_IPS = [
    '80.113.51.130', '213.34.77.18', '195.35.217.210', '80.127.0.49', '213.124.78.74',
    '5.2.199.204', '95.97.137.154', '82.94.225.110', '82.94.170.194', '66.249.64.28',
    '77.163.188.172', '80.113.202.2', '2001:41f0:f70a:1:', '2a02:2f0f:21:101:',
    '2001:888:2085:303:', '2001:470:7d34:40:', '2001:888:2085:303:',
    '2001:984:677c:1:84da:844a:8767:660d']
EXCLUDED_EVENT_VALUE_TYPES = ['productSummary', 'timing', 'productSummary']

MAX_LEN = 100
MAX_DURATION = 1000000


class Session:

    def __init__(self, session_id, clicks, label=None):
        self.session_id = session_id
        self.clicks = clicks
        self.click_count = len(clicks)
        self.entry_time = clicks[0]['timestamp']
        self.duration = clicks[-1]['timestamp'] - self.entry_time
        self.label = label


def filter_fn(line):
    """Determine which clicks are omitted in the analysis

    :param line: dict describing single click
    :return: boolean (False values are filtered)
    """
    if line.get('eventValueType') in EXCLUDED_EVENT_VALUE_TYPES or \
            line.get('tenantHost') != 'www.vakanties.nl' or \
            line.get('info').get('eventTrigger') == 'valueSegment':
        return False
    else:
        return True


def handle_gbk(gbk_result):
    """Sorts the clicks and creates a Session object

    :param gbk_result: tuple of session id and a list of all clicks belonging to a single session
    :return: Session object
    """
    session_id, clicks = gbk_result
    sorted_clicks = sorted(clicks, key=lambda k: k['timestamp'])
    return Session(session_id, sorted_clicks)


def in_market_trigger(click):
    """Determines if the clicks triggers a customer to the inmarket bucket

    :param click: dict
    :return: boolean
    """
    def unix_time_millis(dt):
        return (dt - datetime.utcfromtimestamp(0)).total_seconds() * 1000.0

    timestamp = click['info']['clientTimestamp']
    reservation_status = click['info']['eventTrigger']
    format_period_1 = unix_time_millis(datetime(2018, 6, 20))
    format_period_2 = unix_time_millis(datetime(2018, 10, 1))
    if timestamp < format_period_1:
        return (reservation_status in ['ibe-overview-payment', 'ibe-extras'] or
                'insuranceType' in reservation_status or
                'luggage' in reservation_status or
                'ransfer' in reservation_status)
    elif timestamp < format_period_2:
        return (reservation_status in ['ibe-personaldata', 'ibe-overview-payment'] or
                'insuranceType' in reservation_status or
                'luggage' in reservation_status or
                'ransfer' in reservation_status)
    else:
        return (reservation_status in ['ibe-personaldata', 'ibe-overview-payment',
                                       'changeInsurance', 'changeLuggage',
                                       'changeTransfer', 'transferDetails'])


def float_feature(value):
    """Wraps value(s) into a float list feature"""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def int64_feature(value):
    """Wraps value(s) into a integer list feature"""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    """Wraps single value into a bytes list feature"""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def string_feature(value):
    """Wraps single string value into a bytes list feature"""
    return bytes_feature(value.encode('utf-8'))


def determine_click_features(click):
    """Determines all valuable information from a single click

    :param click: dict
    :return: dict of features
    """
    if click['eventValueJson']:
        event_value_json = json.loads(click['eventValueJson'])
        if type(event_value_json) is not dict:
            event_value_json = {}
    else:
        event_value_json = {}

    def _page_type():
        if click['info']['pagePath'] == '/':
            return 'homepage'
        elif click['info']['pagePath'] == '/zoeken':
            return 'search'
        elif re.match('^/bookings', click['info']['pagePath']):
            return 'booking'
        elif click['info']['pagePath'].count('/') == 1:
            return 'search'
        else:
            return 'productpage'

    page_type = _page_type()

    def _homepage():
        if page_type == 'homepage':
            return 1.0
        else:
            return 0.0

    def _search():
        if page_type == 'search':
            return 1.0
        else:
            return 0.0

    def _productpage():
        if page_type == 'productpage':
            return 1.0
        else:
            return 0.0

    def _event_trigger_feature(feature_name):
        if feature_name == click['info']['eventTrigger']:
            return 1.0
        else:
            return 0.0

    def _event_other():
        if click['info']['eventTrigger'] not in EVENT_TRIGGER_CATEGORIES:
            return 1.0
        else:
            return 0.0

    def _search_sorted_by_feature(values):
        event_value_search = event_value_json.get('search')
        if event_value_search and event_value_search.get('sortedBy') in values:
            return 1.0
        else:
            return 0.0

    def _price_increment():
        event_value_package_availability = event_value_json.get('packageAvailability')
        if event_value_package_availability \
                and event_value_package_availability.get('availablePrice') \
                and event_value_package_availability.get('requestPrice'):
            return event_value_package_availability.get('availablePrice') - \
                   event_value_package_availability.get('requestPrice')
        else:
            return 0.0

    def _timestamp():
        return click['timestamp']

    features = {}

    # Page types
    features['productpage'] = _productpage()
    features['search'] = _search()
    features['homepage'] = _homepage()
    # Event triggers
    for name in EVENT_TRIGGER_CATEGORIES:
        features['event_' + name] = _event_trigger_feature(name)
    features['event_other'] = _event_other()
    # Search sorted by
    features['sorted_by_None'] = _search_sorted_by_feature(['None'])
    features['sorted_by_popularity'] = _search_sorted_by_feature(['popularity'])
    features['sorted_by_dateAscending'] = _search_sorted_by_feature(['date ascending', 'date%20ascending'])
    features['sorted_by_priceAscending'] = _search_sorted_by_feature(['priceAscending', 'priceASC'])
    features['sorted_by_zooverRatingDescending'] = _search_sorted_by_feature(['zooverRatingDescending'])
    features['sorted_by_priceDescending'] = _search_sorted_by_feature(['priceDescending'])
    features['sorted_by_hotelRating'] = _search_sorted_by_feature(['hotelRating'])
    features['sorted_by_price'] = _search_sorted_by_feature(['price'])

    features['price_increment'] = _price_increment()

    features['timestamp'] = _timestamp()

    return features


def determine_features(session):
    """Determines all the features for the model

    :param session: Session object
    :return: a SequenceExample object, see: https://www.tensorflow.org/api_docs/python/tf/train/SequenceExample
    """

    def norm_time_of_day(ts):
        """Normalised time of day"""
        dt = datetime.utcfromtimestamp(ts / 1000)
        return float((dt - dt.today()).seconds) / (60 * 60 * 24)

    def norm_session_length(session_len):
        """Normalised session length"""
        normed = session_len / MAX_LEN
        return normed if normed <= 1 else 1

    def norm_duration(duration):
        """Normalised session duration"""
        normed = duration / MAX_DURATION
        return normed if normed <= 1 else 1

    click_features = [determine_click_features(click) for click in session.clicks]

    feature_dict = {
        'session_id': string_feature(session.session_id),
        'pct_of_day': float_feature(norm_time_of_day(session.entry_time)),
        'total_hits': float_feature(norm_session_length(session.click_count)),
        'duration': float_feature(norm_duration(session.duration))}

    if session.label is not None:
        feature_dict['label'] = int64_feature(session.label)

    for name in CTX_FEATURE_NAMES:
        feature_dict[name] = float_feature(max([click['event_' + name] for click in click_features]))

    hits = [{name: click[name] for name in SEQ_FEATURE_NAMES} for click in click_features]

    ctx_features = tf.train.Features(feature=feature_dict)

    # transpose list of hits to dict of sequence features
    transposed = {}
    for name in SEQ_FEATURE_NAMES:
        if name != 'timestamp':
            transposed[name] = [float_feature(hit[name]) for hit in hits]

    seq_features = tf.train.FeatureLists()
    for k, vs in transposed.items():
        fl = tf.train.FeatureList()
        fl.feature.extend(vs)
        seq_features.feature_list[k].CopyFrom(fl)

    example = tf.train.SequenceExample(context=ctx_features,
                                       feature_lists=seq_features)
    return example


def convert_example_to_prediction(example):
    """Converts the example of features to a json of features (which has the right format for MLengine during prediction

    :param example: SequenceExample
    :return: json of features
    """
    ctx_feature_dict = json.loads(
        json_format.MessageToJson(example.context, including_default_value_fields=True))['feature']
    response = {
        'duration': float(ctx_feature_dict['duration']['floatList']['value'][0]),
        'session_id': ctx_feature_dict['session_id']['bytesList']['value'][0],
        'total_hits': float(ctx_feature_dict['total_hits']['floatList']['value'][0]),
        'pct_of_day': float(ctx_feature_dict['pct_of_day']['floatList']['value'][0])
    }

    if ctx_feature_dict.get('label'):
        response['label'] = int(ctx_feature_dict['label']['int64List']['value'][0])

    for feature_name in CTX_FEATURE_NAMES:
        response['event_' + feature_name] = float(ctx_feature_dict[feature_name]['floatList']['value'][0])

    seq_feature_dict = json.loads(
        json_format.MessageToJson(example.feature_lists, including_default_value_fields=True))['featureList']
    for key, feature_dict in seq_feature_dict.items():
        response[key] = [value['floatList']['value'][0] for value in feature_dict['feature']]

    return response
