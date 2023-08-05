import setuptools
import os
'''
f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))

long_description = f.read()

f.close()

'''
with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentifish", # Replace with your own username
    version="0.0.11",
    author="Aditya Kumar",
    author_email="Adityakumarec@gmail.com",
    description="A simple package for sentiment analysis",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=['pandas','cryptography','pandass'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
