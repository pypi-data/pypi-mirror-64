#! /usr/bin/env python

from setuptools import setup

setup(
    name="dash-okta-oauth2",
    description="Dash Okta OAuth2",
    long_description=open('README.md', 'rt').read().strip(),
    long_description_content_type='text/markdown',
    author="Nico Hein", author_email='nico.hein@me.com',
    url="https://github.com/nicohein/dash-okta-oauth2",
    license='MIT',
    package='dash_okta_oauth2',
    packages=['dash_okta_oauth2'],
    install_requires=[
        'dash>=1.9.1',
        'dash-core-components>=1.8.1',
        'dash-html-components>=1.0.2',
        'Flask>=1.1.1',
        'Flask-Dance>=3.0.0',
        'blinker>=1.4'
    ],
    setup_requires=['pytest-runner', 'setuptools_scm'],
    tests_require=['pytest'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
    use_scm_version=True,
    zip_safe=False,
)
