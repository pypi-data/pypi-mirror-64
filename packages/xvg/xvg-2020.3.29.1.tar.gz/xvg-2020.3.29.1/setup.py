import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xvg",
    version="2020.3.29.1",
    author="Hayden McDonald",
    author_email="lrgstu@gmail.com",
    description="A scriptable vector graphics library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lrgstu/xvgpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
