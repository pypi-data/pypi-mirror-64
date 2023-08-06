from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aioredlock-neorisk',

    version='0.4.0',

    description='Asyncio implemetation of Redis distributed locks (Neorisk)',
    long_description=long_description,

    url='https://github.com/neorisk/aioredlock',

    author='Joan Vilà Cuñat',
    author_email='vila.joan94@gmail.com',

    license='MIT',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='redis redlock distributed locks asyncio',

    packages=find_packages(),

    install_requires=['aioredis', 'attrs >= 17.4.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-asyncio', 'pytest-mock', 'pytest-cov']
)
