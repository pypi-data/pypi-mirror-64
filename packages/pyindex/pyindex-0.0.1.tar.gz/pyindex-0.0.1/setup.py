import setuptools
  

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyindex",
    version="0.0.1",
    author="Anshuman kumar",
    author_email="anshuman@recvani.com",
    description="The search engine for python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anshumankumar/pyindex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=['numpy']
)

