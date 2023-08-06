import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='matplotlib-stream',
    version='1.0.0',
    packages=['matplotlib_stream'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/matplotlib-stream',

    install_requires=[],

    include_package_data=True,
    license='BSD License',
    description="GCPDS: matplotlib stream",
    #    long_description = README,

    classifiers=[

    ],

)
