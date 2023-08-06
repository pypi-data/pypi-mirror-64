import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="salud",
    version="2.4.2020",
    description="Internal PyPi package for mdbrd",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/moodboard/salud",
    author="Moodboard Webmaster",
    author_email="webmaster@mdbrd.in",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    packages=["salud"],
    include_package_data=True,
    install_requires=["vaderSentiment", "nltk", "emoji", "textblob"],
    entry_points={
        "console_scripts": [
            "webmaster-mdbrd=salud.__main__:main",
        ]
    },
)