import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid-19-dryampy", # Replace with your own username
    version="0.3.5",
    author="Steven Yampolsky",
    author_email="syampols@gmail.com",
    description="packages used to throw around covid-19 data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrYampy/covid_19.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)