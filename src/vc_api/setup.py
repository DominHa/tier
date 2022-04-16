import glob
import os

from setuptools import find_packages, setup

install_requires = [
    "fastapi",
    "python-multipart",
    "uvicorn",
    "pydantic",
]

setup(
    name="vehicle_clustering_api",
    version=1,
    url="",
    author="Thomas J Howarth",
    author_email="tom.j.howarth@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    license="Proprietary",
    install_requires=install_requires,
    entry_points={"console_scripts": [""]},
)
