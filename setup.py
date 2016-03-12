import os.path
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('requirements-test.txt') as f:
    required_test = f.read().splitlines()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="whylog_vim",
    version="0.1",
    author="ZPP team",
    author_email="",
    description="whylog_vim v0.1",
    license="BSD 3-clause",
    test_require=required_test,
    install_requires=required,
    url="",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 0 - Alpha",
    ],
    packages=['whylog_vim'],
)
