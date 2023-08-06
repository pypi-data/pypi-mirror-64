import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="pymug",
    version="1.3.0",
    description="A Pymug Joke",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pymug",
    author="Abdur-Rahmaan Janhangeer",
    author_email="arj.python@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["requirements_txt"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["requirements_txt=requirements_txt.__main__:main"]},
)