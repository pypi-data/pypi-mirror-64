from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRED_PACKAGES = [
    'tensorflow>=2.1.0',
    'google',
]

setup(
    name='vaknl-conversion-model',
    description='Conversion model package. Only contains training serving library for now. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0.7',
    url='https://github.com/vakantiesnl/vaknl-PyPi.git',
    author='Merijn van Es',
    author_email='merijn.vanes@vakanties.nl',
    keywords=['vaknl', 'pip'],
    packages=find_packages(),
    python_requires='>=2.7',
    install_requires=REQUIRED_PACKAGES
)
