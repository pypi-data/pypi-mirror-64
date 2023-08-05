import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usefulfunctions",
    version="0.0.1",
    author="Kaz Malhotra",
    author_email="kazmal@protonmail.com",
    description="Some useful functions in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KazMalhotra/usefulfunctions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
