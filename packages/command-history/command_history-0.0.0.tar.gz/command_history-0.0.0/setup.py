import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="command_history",
    version="0.0.0",
    author="Phuc Trinh",
    author_email="trinhcanhphuc@gmail.com",
    description="Get commands history",
    long_description="Get commands history",
    long_description_content_type="text/markdown",
    url="https://github.com/trinhcanhphuc/history.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)