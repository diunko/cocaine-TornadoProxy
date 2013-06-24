#!/usr/bin/env python

from setuptools import setup
setup(
    name="cocaine_tornado_proxy",
    version="0.10.5",
    url="https://github.com/cocaine/cocaine-Tornado-proxy",
    author="Anton Tyurin",
    author_email="noxiouz@yandex.ru",
    packages=["cocaineproxy"],
    license="LGPLv3+",
    scripts=['cocaine-tornado-proxy', 'cocaine-tornado-proxy2'],
    data_files=[('/etc/init.d/',['init/cocaine-tornado-proxy']),
                ('/etc/init.d/',['init/cocaine-tornado-proxy2'])]
)
