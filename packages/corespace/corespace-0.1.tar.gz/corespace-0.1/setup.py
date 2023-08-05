import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corespace",
    version="0.1",
    author="Greg Henry",
    author_email="gregoire.henry@ipsa.fr",
    description="Greg Henry open space toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GregoireHENRY",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
