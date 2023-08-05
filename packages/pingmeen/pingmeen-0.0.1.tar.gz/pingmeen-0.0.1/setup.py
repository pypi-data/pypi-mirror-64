import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                          = "pingmeen", 
    version                       = "0.0.1",
    author                        = "Nikita M. Minaev",
    author_email                  = "nikita.minaev1995@gmail.com",
    description                   = "Pingmeen test package",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "",
    packages                      = setuptools.find_packages(),
    classifiers                   = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires               = '>=3.6',
)