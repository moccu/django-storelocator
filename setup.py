import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-storelocator',
    version='0.1',
    packages=find_packages(),
    zip_safe=False,
    license='MIT',
    description='Django Storelocator is a Django App for locating stores near a geographical location.',
    long_description=open('README.rst').read(),
    url='https://github.com/moccu',
    author='Carlo Smouter',
    author_email='info@moccu.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    dependency_links=['https://github.com/lockwooddev/python-yql'],
    install_requires=[
        "geopy >= 0.95.1",
        "requests >= 1.1.0",
    ],
)
