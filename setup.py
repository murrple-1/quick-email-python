from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='quick-email',
    version='0.1.0',
    description='Quick-and-Dirty Email Sender',
    long_description=long_description,
    url='https://github.com/murrple-1/send-email-python',
    author='Murray Christopherson',
    author_email='murraychristopherson@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='password hashing pbkdf2',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
)
