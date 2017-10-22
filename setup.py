from setuptools import setup

setup(
    name='DuraLex',
    version='0.3',
    install_requires=[
        'colorama',
        'html5lib',
        'beautifulsoup4',
        'requests',
        'unidiff'
    ],
    packages=[
        'duralex'
    ],
    scripts=[
        'bin/duralex'
    ]
)
