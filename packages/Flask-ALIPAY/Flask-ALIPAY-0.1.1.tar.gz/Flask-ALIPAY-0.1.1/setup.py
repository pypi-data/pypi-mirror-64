# -*- coding=utf-8 -*-
from os import path
from codecs import open
from setuptools import setup, find_packages


basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, 'README.md'), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='Flask-ALIPAY',
    version='0.1.1',
    url='https://github.com/luxp4588/flask-alipay.git',
    license='MIT',
    author="python-xp",
    author_email="luxp4588@126.com",
    description="基于flask的支付宝接口",
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['Flask', 'alipay'],
    keywords='flask extension development',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)