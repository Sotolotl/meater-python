import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meater-python",
    version="0.0.1",
    author="Billy Stevenson",
    author_email="meater-api@billystevenson.co.uk",
    description="A wrapper for the Apption Labs Meater probe API v1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/Sotolotl/meater-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)