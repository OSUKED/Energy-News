import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="energynews",
    version="0.0.1",
    author="Ayrton Bourn",
    author_email="ayrton@futureenergy.associates",
    description="EnergyNews is a Python library for retrieving the latest energy journalism",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AyrtonB/Energy-News",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'lxml',
        'beautifulsoup4',
        'ipypb',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)