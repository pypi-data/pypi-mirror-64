# -*- coding: utf-8 -*-
# from setuptools import setup, find_packages
import setuptools
from setuptools import find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='astroimages_file_drivers',
    version='0.1.4',
    description='File handling routines',
    # long_description=readme,
    # long_description_content_type="text/markdown",
    author='Rodrigo de Souza',
    author_email='rsouza01@gmail.com',
    url='https://github.com/AstroImages/astroimages-file-drivers',
    download_url='https://github.com/AstroImages/astroimages-file-drivers/archive/v_0.1.4.tar.gz',
    license=license,
    install_requires=[
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
