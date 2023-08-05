""" setup.py created according to https://packaging.python.org/tutorials/packaging-projects """

import setuptools #type:ignore

with open("README.md", "r") as fh:
    long_description: str = fh.read()

setuptools.setup(
    name="qnlp",
    version="0.0.0",
    author="hashberg",
    author_email="sg495@users.noreply.github.com",
    description="A Python library for Quantum Natural Language Processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hashberg-io/qnlp",
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[ # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    package_data={"": ["LICENSE", "README.md"],
                  "qnlp": ["qnlp/py.typed"],
                 },
    include_package_data=True
)
