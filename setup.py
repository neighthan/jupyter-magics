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

install_path = os.path.join("~", ".ipython", "profile_default", "startup", "ipy_cell_completion_bell.py")
install_path = os.path.expanduser(install_path)

current_dir = os.path.realpath(os.path.dirname(__file__))
source_path = os.path.join(current_dir, "jupyter-utils", "ipy_cell_completion_bell.py")

if os.path.exists(install_path):
    should_copy = input(f"Copy %notify magic to {install_path}? (y/n) ")
    if should_copy:
        shutil.copy(source_path, install_path)
else:
    print(f"Install path for %notify magic not found at {install_path}.")
    print(f"Copy {current_path} to your startup folder manually.")
