from setuptools import setup

setup(
    name='app',
    version='0.1.0',
    py_modules=['app'],
    entry_points={
        'console_scripts': [
            'sql-generate = main:main',
        ],
    },
)