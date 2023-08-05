import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version="0.5.4"

setuptools.setup(
    name="guitarHarmony",
    version=version,
    author="Esparami",
    author_email="heeryerate@gmail.com",
    description="A python wrapper to learn music theory in Guitar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heeryerate/Guitar-Harmony",
    download_url = "https://bitbucket.org/Xi_He/music-theory/get/"+version+".zip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = ['music', 'theory', 'guitar', 'harmony'],
    python_requires='>=3.6',
)
