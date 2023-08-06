import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pltw-3.1.3-nsturtz", # Replace with your own username
    version="0.0.2",
    author="Nathaniel Sturtz",
    author_email="Sturtz110751@indianola.k12.ia.us",
    description="My first Mod",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sturtz.ddns.net/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
