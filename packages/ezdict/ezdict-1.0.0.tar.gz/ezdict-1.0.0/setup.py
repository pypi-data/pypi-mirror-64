import setuptools

with open("README.md", "r") as file:
    long_desc = file.read()

setuptools.setup(
    name="ezdict",
    version="1.0.0",
    author="Jacob Morris",
    author_email="blendingjake@gmail.com",
    description="Making Python's `dict` easier to work with by adding object notation and grouping",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/BlendingJake/EZDict",
    packages=["ezdict"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires=">=3.5"
)
