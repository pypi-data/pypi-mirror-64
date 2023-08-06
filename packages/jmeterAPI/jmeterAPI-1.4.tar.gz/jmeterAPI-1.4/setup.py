#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from os.path import join


def fetch_xml_path():
    #path_here = os.getcwd()
    #path_projects = os.path.join(path_here, "jmeter_api")
    file_list = ["include README.md LICENSE", "recursive-include tests *.py"]
    for root, dirs, files in os.walk("jmeter_api"):
        for file in files:
            if file.endswith(".xml"):
                path_xml = os.path.join(root,file)
                file_list.append(path_xml)
    with open("MANIFEST.in", "w") as file:
        [file.write(f"include {i}\n") for i in file_list]
    return file_list

fetch_xml_path()

with open('README.md', 'r') as f:
    README = f.read()
# with open('HISTORY.md', 'r', 'utf-8') as f:
#     history = f.read()


setup(
    name='jmeterAPI',
    version='1.4',
    description='JMeter test plan builder',
    long_description=README,
    author='Alexey Svetlov',
    author_email='alexeysvetlov92@gmail.com',
    #url='https://github.com/lanitgithub/jmeter_api',
    # license='MIT',
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'atomicwrites', 'attrs', 'colorama',
        'importlib-metadata', 'Jinja2', 'MarkupSafe',
        'more-itertools', 'packaging', 'pluggy',
        'py', 'pytest', 'pyparsing', 'python-dateutil', 'six', 
        'wcwidth', 'xmltodict','zipp',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        # 'Documentation': 'https://requests.readthedocs.io',
        'Source': 'https://github.com/lanitgithub/jmeter_api',
    },
)
