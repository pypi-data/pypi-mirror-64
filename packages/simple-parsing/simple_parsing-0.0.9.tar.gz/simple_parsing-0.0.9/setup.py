import sys
import setuptools

with open("README_pypi.md", "r") as fh:
    long_description = fh.read()
packages = setuptools.find_namespace_packages(include=['simple_parsing*'])
print("PACKAGES FOUND:", packages)
print(sys.version_info)

setuptools.setup(
    name="simple_parsing",
    version="0.0.9",
    author="Fabrice Normandin",
    author_email="fabrice.normandin@gmail.com",
    description="A small utility for simplifying and cleaning up argument parsing scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lebrice/SimpleParsing",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['dataclasses'] if sys.version_info < (3, 7) else [],
)
