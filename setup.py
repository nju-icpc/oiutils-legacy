from setuptools import Command, setup

setup(
    name = 'Oiutils',
    version = '0.1',
    license = 'GPLv2',
    packages = ['oi', 'oi.contest'],
    install_requires = [
        'pyyaml'
    ],
    entry_points = '''
        [console_scripts]
        oi = oi.cli:main
    '''
)
