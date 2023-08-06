#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

from cmt import static_data

# get long description
with Path('README.rst').open(mode='r', encoding='UTF-8') as reader:
    LONG_DESCRIPTION = reader.read()

setup(
    name=static_data.NAME,
    version=static_data.VERSION,
    description=static_data.DESCRIPTION,
    long_description_content_type='text/x-rst',
    long_description=LONG_DESCRIPTION,
    author=static_data.AUTHOR,
    author_email=static_data.AUTHOR_EMAIL,
    license='MIT',
    url=static_data.PROJECT_URL,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    keywords='map toolkit',
    packages=find_packages(include=['cmt', 'cmt.*']),
    python_requires='>=3.7',
    install_requires=[
    ],
    extras_require={
        'dev': [
            'flake8==3.7.9',
            'pylint==2.4.4',
            'pyroma==2.6',
            'pytest==5.4.1',
            'pytest-cov==2.8.1',
            'Sphinx==2.4.4',
            'sphinx-autodoc-typehints==1.10.3',
            'sphinx_rtd_theme==0.4.3',
            'twine==3.1.1',
            'setuptools==46.1.3',
            'wheel==0.34.2',
        ],
    },
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'cmt = cmt.cs.main:main',
        ],
    },
)
