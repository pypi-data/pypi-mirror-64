import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taiga-bio",
    version="1.0.1",
    author="Maycon Oliveira",
    author_email="flayner5@gmail.com",
    description="Set of tools to fetch taxonomic metadata for a list of organisms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flayner2/taiga-bio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Bio-Informatics"],
    python_requires=">=3.6"
)
