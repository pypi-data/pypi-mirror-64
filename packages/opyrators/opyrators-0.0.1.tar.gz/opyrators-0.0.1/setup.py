import setuptools

long_description = "Opyrators (pronounced the same way as the word 'operators') is a lightweight python package that represents many-body fermionic and spin operators as strings. Complex commutators can easily be computed with opyrators, see the github repository for examples."

setuptools.setup(
    name="opyrators",
    version="0.0.1",
    author="Evert van Nieuwenburg",
    author_email="evert.v.nieuwenburg@gmail.com",
    description="Manipulate quantum many-body operators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/everthemore/opyrators",
    packages=setuptools.find_packages(),
    setup_requires=["numpy"],
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
