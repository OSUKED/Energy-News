import setuptools

with open("satip/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="satip",
    version="0.0.5",
    author="Ayrton Bourn",
    author_email="ayrton@futureenergy.associates",
    description="Satip is a Python library for satellite image processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Future-Energy-Associates/satellite_image_processing", # change after merging back to ocf
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)