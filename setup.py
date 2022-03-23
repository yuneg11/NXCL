from setuptools import setup

with open("nxcl/__init__.py") as init_file:
    __version__ = ""
    # extract __version__
    for line in init_file:
        if line.startswith("__version__"):
            exec(line)
            break


with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    name="nxcl",
    version=__version__,
    author="EungGu Yun",
    author_email="yuneg11@gmail.com",
    description="NXCL is an eXperiment Core Library",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yuneg11/NXCL",
    project_urls={
        "Bug Tracker": "https://github.com/yuneg11/nxcl/issues"
    },
    packages=["nxcl"],
    package_dir={"nxcl": "nxcl"},
    # package_data={'': []},
    # include_package_data=True,
    license="MIT license",
    python_requires=">=3.7",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
)
