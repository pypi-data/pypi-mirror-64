import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="klib",
    version="0.0.2",
    author="Andreas Kanz",
    author_email="andreas@akanz.de",
    description="Frequently used custom data science functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akanz1/klib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)