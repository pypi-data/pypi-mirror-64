from setuptools import find_packages, setup


with open("requirements.txt") as f:
    requirements = [x for x in f.read().split("\n") if x and not x.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()


version = "1.1.3"

setup(
    name="py_presi",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
    install_requires=requirements,
    entry_points={"console_scripts": [
        "pp-build = py_presi.__main__:build"
    ]},
)
