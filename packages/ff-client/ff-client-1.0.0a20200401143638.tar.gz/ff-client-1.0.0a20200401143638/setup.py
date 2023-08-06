import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ff-client",
    version="1.0.0.a20200401143638",
    author="Elliot Levin",
    author_email="elliotlevin@hotmail.com",
    description="Client library for ff-proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TimeToogo/ff-proxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)