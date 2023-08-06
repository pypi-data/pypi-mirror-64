import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid_vir_assistant",
    version="0.0.2",
    author="TrinhAnBinh",
    author_email="binhta1995@gmail.com",
    description="A small example about virtual assitant like Siri/ Google assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TrinhAnBinh/covid_vir_assistant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)