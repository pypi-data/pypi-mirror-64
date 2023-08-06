from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='bRusky',
    version='0.3.6',
    packages=find_packages(),
    install_requires=[
    'requests',
    'transliterate',
    'pysocks',
    'requests[socks]',
    ],
    entry_points={
        'console_scripts':
            ['bRusky = bRusky.commands:bRusky']
    }
)