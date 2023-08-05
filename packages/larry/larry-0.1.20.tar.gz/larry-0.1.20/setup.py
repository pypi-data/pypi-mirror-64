import setuptools
import larry as lry

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="larry",
    version=lry.__version__,
    author="Dave Schultz",
    author_email="djschult@gmail.com",
    description="Library of helper modules for common data tasks using AWS resources such as S3, SQS, MTurk and others",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschultz0/larry",
    packages=setuptools.find_packages(),
    keywords="larry data aws boto3 mturk s3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
