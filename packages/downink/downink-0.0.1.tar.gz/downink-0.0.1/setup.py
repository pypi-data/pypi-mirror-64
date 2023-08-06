from os import path
from setuptools import setup

current = path.abspath(path.dirname(__file__))
with open(path.join(current, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(current, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name='downink',
    license='MIT',
    version='0.0.1',
    author='mentix02',
    packages=['downink'],
    scripts=['bin/downink'],
    python_requires='>=3.2',
    long_description=long_description,
    install_requires=install_requires,
    author_email='manan.yadav02@gmail.com',
    url='http://github.com/mentix02/downink',
    long_description_content_type='text/markdown',
    description='Download resources from the internet with a single command.',
)
