import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwordmaker-pkg-leonardomartelli",
    version="0.0.1",
    author="Leonardo Martelli Oliveira",
    author_email="lmartellioliveira@gmail.com",
    description="A Password Maker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardomartelli/passwordmaker_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)