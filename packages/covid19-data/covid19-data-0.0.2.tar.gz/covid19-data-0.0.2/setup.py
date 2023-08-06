from setuptools import setup
import setuptools

setup(
    name='covid19-data',
    version='0.0.2',
    description='A fast, powerful, and flexible way to get up to date COVID-19 data for any major city, state, '
                'country, and total world wide data',
    long_description='Gets data for CoronaVirus (COVID-19) using John Hopkins\' ArcGIS application layer  '
                     'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer '
                     'using a '
                     'query to return a JSON document, so unlike similar packages it does not rely on a datasheet '
                     'that is might not be up to date, but queries the source database directly. This allows us to '
                     'get the most up to date information that is currently available, as well enabling us t'
                     'o get any of the data we want without any that is not wanted.',
    url='http://github.com/binarynightowl/covid19_python',
    author='Taylor Dettling',
    author_email='taylor@binarynightowl.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['json', 'urllib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
