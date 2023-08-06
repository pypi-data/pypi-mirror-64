import setuptools
from setuptools import setup

setup(
    name="stark",
    version="0.0.1",
    author="Iheb Haboubi",
    author_email="iheb.haboubi56@gmail.com",
    description="stark generates random and strong passwords",
    url="https://github.com/Iheb-Haboubi/stark",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["stark=stark.app:main"],},
)
