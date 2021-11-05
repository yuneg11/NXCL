from setuptools import setup

with open("nxpl/__init__.py") as init_file:
    __version__ = ""
    # extract __version__
    for line in init_file:
        if line.startswith("__version__"):
            exec(line)
            break


with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    name="nxpl",
    version=__version__,
    author="EungGu Yun",
    author_email="yuneg11@gmail.com",
    description="NXPL is eXperiment PipeLine",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yuneg11/nxpl",
    project_urls={
        "Bug Tracker": "https://github.com/yuneg11/nxpl/issues"
    },
    packages=["nxpl"],
    package_dir={"nxpl": "nxpl"},
    package_data={'': ["default.yaml"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "nxpl=nxpl.cli.cli:cli",
        ]
    },
    license="MIT license",
    python_requires=">=3.7",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
    ],
)
