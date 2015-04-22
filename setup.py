from setuptools import Command, setup

setup(
    name = 'Oiutils',
    version = '0.1',
    license = 'GPLv2',
    packages = ['oi', 'oi.contest', 'oi.sandbox', 'oi.compile', 'oi.judge'],
    install_requires = [
        'pyyaml', 'psutil'
    ],
    entry_points = '''
        [console_scripts]
        oi = oi.cli:main
    '''
)
