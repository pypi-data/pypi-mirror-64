#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from setuptools import setup
from utils import find_packages, find_package_data, read_md, package_attr

PACKAGE_NAME = "nimbus_setup"

EXCLUDE = ("*.pyc", "*.pyo",)
INCLUDE = ("*.po", "*.mo", "*.md", "*.txt", "*.html", "*.js", "*.css")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PREFIX_DIR = BASE_DIR
PACKAGE_DIR = os.path.join(PREFIX_DIR, PACKAGE_NAME)
README = os.path.join(BASE_DIR, "README.md")

version = package_attr(PACKAGE_NAME, "version")


def clean():
    shutil.rmtree("{}/dist".format(PREFIX_DIR), ignore_errors=True)
    shutil.rmtree("{}/build".format(PREFIX_DIR), ignore_errors=True)
    shutil.rmtree("{}/{}.egg-info".format(PREFIX_DIR, PACKAGE_NAME), ignore_errors=True)


def git_push():
    os.system("git add {}".format(PACKAGE_DIR))
    os.system("git commit -m '{}' {}".format(version, PACKAGE_DIR))
    os.system("git tag -a {} -m 'version {}'".format(version, version))
    os.system("git push --tags")
    os.system("git push")


if sys.argv[-1] == "clean":
    clean()
    sys.exit()

elif sys.argv[-1] == 'preinstall':
    os.system("pip install pypandoc twine")
    sys.exit()

elif sys.argv[-1] == "publish":
    try:
        import pypandoc
    except ImportError as e:
        print("pypandoc not installed.\nUse `pip install pypandoc`.\nExiting.")
        raise e
    try:
        import twine
    except ImportError as e:
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        raise e
    os.system("python setup.py bdist_wheel")
    os.system("twine upload {}/dist/*".format(PREFIX_DIR))
    # os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")

    clean()
    git_push()
    sys.exit()

###################################################################
os.chdir(PREFIX_DIR)

setup(
    name=PACKAGE_NAME,
    version=version,

    url=package_attr(PACKAGE_NAME, attr="url"),
    license=package_attr(PACKAGE_NAME, attr="license"),
    copyright=package_attr(PACKAGE_NAME, attr="copyright"),

    description=package_attr(PACKAGE_NAME, attr="description"),
    long_description=read_md(README),

    author=package_attr(PACKAGE_NAME, attr="author"),
    author_email=package_attr(PACKAGE_NAME, attr="author_email"),
    keywords=package_attr(PACKAGE_NAME, attr="keywords"),
    platforms=package_attr(PACKAGE_NAME, attr="platforms"),

    packages=find_packages(PACKAGE_DIR, prefix=PREFIX_DIR, exclude=EXCLUDE),
    package_data=find_package_data(PACKAGE_DIR, prefix=PREFIX_DIR, exclude=EXCLUDE, include=INCLUDE),
    install_requires=package_attr(PACKAGE_NAME, attr="install_requires"),

    classifiers=package_attr(PACKAGE_NAME, attr="classifiers"),
    zip_safe=package_attr(PACKAGE_NAME, attr="zip_safe"),
)
