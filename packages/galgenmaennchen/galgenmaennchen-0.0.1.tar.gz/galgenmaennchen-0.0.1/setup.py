import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="galgenmaennchen", 
    version="0.0.1",
    author="Leo Blume",
    author_email="leoblume@gmx.de",
    description="Ein Galgenmännchenspiel für dich.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/galgenmaennchen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Development Status :: 4 - Beta",
        "Natural Language :: German",
        "Topic :: Games/Entertainment :: Board Games"
    ],
    python_requires='>=3.0',
)