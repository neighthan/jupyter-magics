from pathlib import Path

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jupyter-magics",
    version="0.1",
    author="Nathan Hunt",
    author_email="neighthan.hunt@gmail.com",
    description="Utility functions for Jupyter notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neighthan/jupyter-magics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

install_dir = Path.home() / ".ipython" / "profile_default" / "startup"
source_dir = Path(__file__).resolve().parent / "jupyter_magics"

for file in source_dir.glob("*"):
    fname = file.name
    if fname == "__init__.py": continue
    source_path = source_dir / fname
    install_path = install_dir / fname
    if fname.endswith(".py"):
        install_path.write_text(source_path.read_text())
    else:
        install_path.write_bytes(source_path.read_bytes())
