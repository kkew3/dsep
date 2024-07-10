from setuptools import setup

setup(
    name='dsep',
    py_modules=['dsep'],
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'dsep = dsep:app',
        ],
    },
)
