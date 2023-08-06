import setuptools

with open('README.md') as f:
    longDescription = f.read()

setuptools.setup(
    name="swapnilpkg",
    version="0.0.1",
    author="Swapnil Raut",
    author_email="swapnil.purandar@gmail.com",
    description="My personal package",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)
