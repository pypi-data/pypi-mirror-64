import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="talisestools",
    version="0.0.3",
    author="Sascha Vowe",
    author_email="vowe@mail.de",
    description="Tools for handling TAELISES generated binary data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/savowe/talisestools",
    packages=['talisestools'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)