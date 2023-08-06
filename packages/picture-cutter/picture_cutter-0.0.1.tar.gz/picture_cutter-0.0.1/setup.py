import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="picture_cutter",
    version="0.0.1",
    author="debuglevel",
    author_email="debuglevel@gmail.com",
    description="Package to cut picture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debuglevel/picture_cutter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
