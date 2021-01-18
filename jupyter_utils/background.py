"""
Adds a magic to IPython which will run all of the code in the current notebook up until
the current cell in a new process.
Put this file in, e.g., ~/.ipython/profile_default/startup to load this magic on startup.
"""

import json
from os.path import dirname
from subprocess import Popen
from tempfile import NamedTemporaryFile
from time import sleep

from IPython.core.magic import register_cell_magic

from .jupyter_utils import get_notebook_path


@register_cell_magic
def background(line: str, cell: str):
    """
    Any cells with cell magics will be skipped (in case it's something like %%bash) as
    will any lines with line magics. The exception is that the rest of the code in the
    cell that's running this magic will be included.
    """
    nb_fname = get_notebook_path()
    if nb_fname is None:
        raise RuntimeError("Unable to find path to current notebook.")

    with open(nb_fname) as f:
        nb = json.load(f)

    code = ""

    terminate = False
    for cell in nb["cells"]:
        # skip markdown and empty code cells
        if cell["cell_type"] != "code" or not cell["source"]:
            continue

        if cell["source"][0].startswith("%%"):
            if cell["source"][0].startswith("%%background"):  # end after this cell
                cell["source"] = cell["source"][1:]  # skip the line with the magic
                terminate = True
            else:  # skip cells with any other cell magics; this might, e.g., be something like %%bash
                continue

        # skip line magics
        code += (
            "".join([line for line in cell["source"] if not line.startswith("%")])
            + "\n"
        )
        if terminate:
            break

    # execute code, from the same directory in case relative paths are used
    with NamedTemporaryFile("w", dir=dirname(nb_fname)) as tmp:
        tmp.write(code)
        tmp.seek(0)  # running cat didn't show anything unless I did this

        Popen(["python", tmp.name])
        # otherwise, it seems like the file is deleted before Popen even gets to it
        sleep(0.5)
