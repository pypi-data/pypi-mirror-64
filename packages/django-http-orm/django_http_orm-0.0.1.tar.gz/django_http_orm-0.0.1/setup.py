import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="django_http_orm",
    version="0.0.1",
    author="Alex Lang",
    author_email="alex.lang@gmail.com",
    description="A simple HTTP interface over Django ORM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/langal/django_http_orm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
