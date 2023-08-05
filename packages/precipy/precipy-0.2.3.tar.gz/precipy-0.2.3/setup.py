import setuptools

setuptools.setup(
    name="precipy",
    version="0.2.3",
    author="Ana Nelson",
    author_email="ana@ananelson.com",
    url="https://github.com/ananelson/precipy",
    packages=setuptools.find_packages(),
    install_requires = [
        "jinja2",
        "markdown",
        "pygments"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
