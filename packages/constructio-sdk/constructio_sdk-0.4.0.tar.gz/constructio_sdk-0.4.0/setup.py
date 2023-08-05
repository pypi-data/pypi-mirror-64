import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="constructio_sdk", # Replace with your own username
    version="0.4.0",
    author="Olivier Hoareau",
    author_email="oha+oss@greenberets.io",
    description="Constructio SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amocer-idf/constructio-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)