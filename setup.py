"""
Automatically set up the project for development.
"""

from setuptools import setup, find_packages

setup(
    name="environ",
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy",
        "pandas",
        "matplotlib",
        "tqdm",
    ],
    extras_require={
        "dev": [
            "pylint",
            "black",
        ]
    },
)
