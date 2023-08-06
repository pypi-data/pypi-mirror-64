import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cjkstr", # Replace with your own username
    version="0.0.5",
    author="Shin-Wei Hwang",
    author_email="meebox@gmail.com",
    description="A simple package to processing CJK string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codemee/cjkstr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
