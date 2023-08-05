import setuptools

setuptools.setup(
    name="precipy",
    version="0.2.2",
    author="Ana Nelson",
    author_email="ana@ananelson.com",
    url="https://github.com/ananelson/precipy",
    packages=setuptools.find_packages(),
    install_requires = [
        "google-cloud-storage",
        "jinja2",
        "markdown",
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
