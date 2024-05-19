import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scimate",
    version="0.0.1",
    author="Riccardo Galafassi",
    author_email="riccardo.galafassi@univ-lyon1.fr",
    description="Scientific tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7.0",
    install_requires=[
        'pandas',
        'numpy'
    ],
)