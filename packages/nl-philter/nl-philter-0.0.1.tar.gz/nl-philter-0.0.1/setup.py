from setuptools import setup, find_packages

setup(
    name="nl-philter",
    version="0.0.1",
    description="cLUT/Cube toolkit for recording color transformations.",
    author="nonlogicaldev",

    install_requires=[
        "numpy>=1.16.2",
        "Pillow>=6.2.0",
    ],

    packages=find_packages(),
    scripts=[
        "bin/philter"
    ]
)

