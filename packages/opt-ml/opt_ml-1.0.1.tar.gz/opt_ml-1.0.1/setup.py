import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opt_ml",  # Replace with your own username
    version="1.0.1",
    author="Anish Acharya",
    author_email="anishacharya@utexas.edu",
    description="Optimization Tools for Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anishacharya/OptExp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')