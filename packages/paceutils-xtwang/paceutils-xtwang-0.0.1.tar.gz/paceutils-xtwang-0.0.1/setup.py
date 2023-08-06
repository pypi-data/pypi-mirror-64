import setuptools
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paceutils-xtwang", # Replace with your own username
    version="0.0.1",
    author="Alex Xin Tong Wang",
    author_email="XinTong.Wang@riotinto.com",
    description="Python utility package for PACE Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://upload.pypi.org/legacy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'setuptools',
        'boto3',
        'statsmodels',
        ''
    ]
)