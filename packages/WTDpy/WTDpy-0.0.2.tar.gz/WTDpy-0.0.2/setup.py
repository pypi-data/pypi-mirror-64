"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["pandas", "httpx"]

setup_requirements = ["pytest-runner"]

test_requirements = [
    "pytest",
    "pytest-cov",
    "pytest-timeout",
    "black",
    "isort",
    "pylama",
]

setup(
    author="Joris den Uijl",
    author_email="jorisdenuijl@gmail.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    description="Basic calls to the World Trading Data API with Python.",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=["wtdpy", "world trading data", "API"],
    name="WTDpy",
    packages=find_packages(include=["wtdpy"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/uijl/wtdpy",
    version="0.0.2",
    zip_safe=False,
)
