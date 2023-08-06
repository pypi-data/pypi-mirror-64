import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bgu_aws",
    version="0.0.4",
    author="Assaf Arbelle",
    author_email="arbellea@post.bgu.ac.il",
    description="Utilities for AWS code managements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/arbellea/bgu-aws-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['requests'],
)
