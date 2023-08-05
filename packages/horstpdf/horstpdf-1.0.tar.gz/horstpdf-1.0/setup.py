import setuptools
from pathlib import Path

setuptools.setup(
    name="horstpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packetages=setuptools.find_packages(exclude=["tests", "data"])

)