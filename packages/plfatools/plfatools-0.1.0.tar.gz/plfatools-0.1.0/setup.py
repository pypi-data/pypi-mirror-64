import setuptools
import pathlib

# Read the README file
this_directory = pathlib.Path(__file__).parent
with open((this_directory / 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
  name = 'plfatools',
  packages = setuptools.find_packages(),
  version = '0.1.0',
  license='CC0',
  description = 'This package automates the aggregation of output from MIDI Inc. Sherlock PLFA Analysis Software into a single csv file.',
  author = 'Patrick Morrell, Bryan Carlson',
  author_email = 'bryan.carlson@usda.gov',
  url = 'https://github.com/cafltar/plfa_tools_aggregator',
  download_url = 'https://github.com/cafltar/plfa_tools_aggregator.git',
  keywords = ['Aggregator', 'PLFA', 'CSV'],
  install_requires=  ['pathlib', 'pandas', 'numpy'],
  entry_points = {"console_scripts": ["plfatools=plfatools.__main__:main"]},
  long_description = long_description,
  long_description_content_type='text/markdown',
  classifiers=[
    'Development Status :: 4 - Beta',     
		'Intended Audience :: Science/Research',      
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',  
		'Programming Language :: Python :: 3'
  ],
)