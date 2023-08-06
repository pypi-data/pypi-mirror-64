import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('tax2proteome/version.py').read())

setuptools.setup(
    name="tax2proteome", 
    version=__version__,
    author="Juliane Schmachtenberg",
    author_email="jule-schmachtenberg@web.de",
    description="tax2proteome creates based on given taxon IDs and a reference database a taxon specific database in fasta format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jschmacht/tax2proteome",
    packages=setuptools.find_packages(),
    classifiers=[
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['biopython', 'tqdm', 'wget'],
    python_requires='~=3.6',
)