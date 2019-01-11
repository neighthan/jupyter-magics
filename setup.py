import setuptools
import os
import shutil

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jupyter-utils",
    version="0.1",
    author="Nathan Hunt",
    author_email="neighthan.hunt@gmail.com",
    description="Utility functions for Jupyter notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neighthan/jupyter-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

install_dir = os.path.join("~", ".ipython", "profile_default", "startup")
install_dir = os.path.expanduser(install_dir)
install_path = os.path.join(install_dir, "ipy_cell_completion_bell.py")

current_dir = os.path.realpath(os.path.dirname(__file__))
source_path = os.path.join(current_dir, "jupyter_utils", "ipy_cell_completion_bell.py")

try:
    shutil.copy(source_path, install_path)
except (FileNotFoundError, PermissionError, shutil.SameFileError):
    print(f"Unable to install %notify magic to {install_dir}.")
    print(f"Copy {source_path} to your startup folder manually.")
