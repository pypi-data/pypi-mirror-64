from setuptools import setup, find_packages
from platform import python_version_tuple
import sys, os

version = '0.1'

setup(
    name='suber',
    version=version,
    description="Tool to find subtitles",
    keywords='opensubtitles python api',
    author='Suparno Karmakar',
    author_email='ssuparno1998@gmail.com',
    url='https://github.com/Suparno1998/subd',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    extras_require={
        'Support for encoding detection on downloaded subtitle':
            [
                'charset_normalizer' if int(python_version_tuple()[0]) >= 3 else 'chardet'
            ],
    }
)