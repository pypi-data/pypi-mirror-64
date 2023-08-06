
from setuptools import setup, find_packages


with open("README.md", "r") as fp:
    long_description = fp.read()


setup(
    name="qb",
    version="0.0",
    author="Miloslav Pojman",
    author_email="miloslav.pojman@gmail.com",
    description="SQL query builder",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    zip_safe=False,
    include_package_data=True,
)
