from setuptools import setup, find_packages

setup(
    name="mcdm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "pytest>=6.2.5",
        "pymcdm>=0.1.0",
    ],
) 