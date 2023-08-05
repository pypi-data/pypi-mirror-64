import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GOSH-FHIRworks2020-SkypeURI", # Replace with your own username
    version="0.0.1",
    author="Alexandru-Vlad Niculae",
    author_email="43644109+AlexNiculae@users.noreply.github.com",
    description="GOSH FHIR Hackathon API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexNiculae/GOSH-FHIRworks2020-SkypeURI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)