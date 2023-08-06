import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cldpy",
    version="0.0.8",
    author="cloudpy.io",
    author_email="author@example.com",
    description="cloudpy.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ortutay/cldpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
