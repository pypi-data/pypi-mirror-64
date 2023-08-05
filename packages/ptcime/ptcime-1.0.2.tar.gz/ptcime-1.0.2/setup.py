import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptcime", # Replace with your own username
    version="1.0.2",
    author="Pedro Tavares de Carvalho",
    author_email="ptcar2009@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ptcar2009/ptcime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["./scripts/ptcime"],
    python_requires='>=3.6',
)