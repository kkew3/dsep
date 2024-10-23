from setuptools import setup, find_packages

setup(
    name='dsep',
    packages=find_packages(),
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'dsep = dsep.dsep:app',
        ],
    },
    install_requires=[
        'click',
        'pyparsing',
        'networkx>=3.3',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)
