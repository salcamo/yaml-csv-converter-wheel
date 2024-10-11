from setuptools import setup, find_packages

setup(
    name='yaml-csv-converter',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'yaml-csv-converter = yaml_csv_converter.converter:main',
        ],
    }
)
