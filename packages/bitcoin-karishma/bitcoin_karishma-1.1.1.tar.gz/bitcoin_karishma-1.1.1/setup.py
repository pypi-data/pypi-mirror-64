from setuptools import setup


# function to open & read the README.md file
def readme():
    with open('README.md') as f:
        README = f.read()
    return README


# this part contains details of the package/module like which license, version of python, libraries, etc
# that are needed for running  the package also info about the author
setup(
    name="bitcoin_karishma",
    version="1.1.1",
    description="A Python package to get bitcoin updates and predictions",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/karishma-garg-au7/bitcoin_notification",
    author="Karishma Agarwal",
    author_email="karishmaag21@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bitcoin_karishma"],
    include_package_data=True,
    install_requires=["requests", "datetime"],
    entry_points={
        "console_scripts": [
            "bitcoin_karishma=bitcoin_karishma.run:main",
        ]
    },
)