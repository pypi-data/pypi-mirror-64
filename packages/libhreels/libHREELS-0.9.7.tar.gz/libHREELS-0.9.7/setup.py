import setuptools

with open("libHREELS/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libHREELS",
    version="0.9.7",
    author="Wolf Widdra",
    author_email="wolf.widdra@gmx.de",
    description="Handling, simulating, and plotting HREELS and Auger spectroscopy data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.informatik.uni-halle.de/e3fm8/libHREELSnew",
    packages=setuptools.find_packages(),
	include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)