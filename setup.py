import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="python-steamgriddy",
    version="1.0.5",
    author="Michael DeGuzis",
    author_email="mdeguzis@gmail.com",
    description="Update,fix, and replace your games Steam artwork.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdeguzis/python-steamgriddy",
    install_requires = [
        'requests>=2.28.1',
        'vdf',
        'xmltodict'
    ],
    packages=setuptools.find_packages(),
    license="MIT",
    keywords=['steamgriddb', 'steamgrid', 'steamgriddy', 'steam', 'grid', 'db', 'api', 'wrapper'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
