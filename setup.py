#!/usr/bin/env python
from setuptools import Command, setup

setup(
    name = 'Oiutils',
    version = '0.1',
    license = 'GPLv2',
    packages = ['oi',
        'oi.contest',
        'oi.sandbox',
        'oi.compile',
        'oi.judge',
        'oi.remote',
        'oi.fc',
        'oi.visual'],
    package_data = {
        'oi.visual': [
            'templates/*.html', 'static/js/*.js', 'static/css/*.css',
        ],
    },
    install_requires = [
        'pyyaml', 'psutil', 'flask',
    ],
    entry_points = {
        'console_scripts': [
            'oi = oi.cli:main',        
        ],
    }
)
