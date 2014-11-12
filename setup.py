from setuptools import Command, setup

setup(
    name = 'Oiutils',
    version = '0.01',
    license = 'GPLv2',
    packages = ['oi'],
    install_requires = [
    ],
    entry_points = '''
        [console_scripts]
        oi = oi.cli:main
    '''
)
