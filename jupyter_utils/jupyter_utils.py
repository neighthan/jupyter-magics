import json
import os.path
import re
import ipykernel
import requests
from urllib.parse import urljoin
from notebook.notebookapp import list_running_servers
from typing import List, Dict, Optional, Any, Callable
import inspect


def get_notebook_name():
    """
    Return the full path of the jupyter notebook.
    
    From https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246.
    """
    kernel_id = re.search(
        "kernel-(.*).json", ipykernel.connect.get_connection_file()
    ).group(1)
    servers = list_running_servers()
    for server in servers:
        response = requests.get(
            urljoin(server["url"], "api/sessions"), params={"token": server.get("token", "")}
        )
        for notebook in json.loads(response.text):
            if notebook["kernel"]["id"] == kernel_id:
                relative_path = notebook["notebook"]["path"]
                return os.path.join(server["notebook_dir"], relative_path)


def get_nb_imports(nb_name: str) -> dict:
    """
    Find all lines in a Jupyter notebook which are imports.

    Return a dictionary like
    {('pd',): 'import pandas as pd',
     ('roc_auc_score', 'roc_curve'): 'from sklearn.metrics import roc_auc_score, roc_curve'}

    Assumes each import statement is one line, which doesn't actually have to be the case.
    This will also get confused if you have, e.g., strings that look like imports
    (s = "import pandas as pd"); you'll get some error then.
    """

    with open(nb_name) as f:
        cells = json.loads(f.read())["cells"]

    import_lines = []
    for cell in cells:
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        assert type(source) == list
        for line in source:
            line = line.strip()

            if line.startswith("#"):
                continue

            words = line.split(" ")

            if words[0] == "import" or (words[0] == "from" and words[2] == "import"):
                import_lines.append(line)

    imported_names = []
    for line in import_lines:
        words = line.split(" ")
        if words[0] == "import":  # ex import time or import numpy as np
            imported_names.append((words[-1],))
        else:  # ex from sklearn.metrics import roc_auc_score, roc_curve
            imported_names.append(
                tuple(
                    word.replace(",", "") for word in words[words.index("import") + 1 :]
                )
            )

    return {imported_names[i]: import_lines[i] for i in range(len(imported_names))}


def write_funcs_to_file(
    fname: str, funcs: List[Callable], local_vars: Optional[Dict[str, Any]] = None
) -> None:
    """
    Write the source for `funcs` in a file at `fname`, including imports.
    A best-effort attempt is made at including any imports needed for your functions to run; there
    are several caveats to this (see `get_nb_imports` for more information).
    :param fname: path to the file to write the functions in
    :param funcs: a list of functions whose source code should be written in the file at fname
    :param local_vars: just set local_vars=locals() if using this.
      If provided, a check is done for each local function (unless it's imported)
      to determine if one of the functions in `funcs` calls it; if so, an AssertionError is raised.
      You can add these functions to `funcs` or set `local_vars` to `None` to ignore this.
      Note that this is a best-effort check and may not catch all cases or may raise errors when
      there are no problems.
    """

    imports_needed = set()
    source = []
    imports = get_nb_imports(get_notebook_name())

    for func in funcs:
        source_lines = inspect.getsourcelines(func)[0]

        for import_names in imports:
            for import_name in import_names:
                for line in source_lines:
                    if import_name not in line:
                        continue

                    # we have to be a little careful here; some short import
                    # names like np or pd may show up by chance in another word,
                    # so we don't just want to check that the name occurs _anywhere_
                    # these checks should help, though there will still be
                    # errors possible

                    function_call = f"{import_name}("
                    module_use = f"{import_name}."
                    if (
                        function_call in line
                        or module_use in line
                        or len(import_name) > 3
                    ):
                        imports_needed.add(imports[import_names] + "\n")

        source.extend(source_lines)
        source.extend(["\n"] * 2)

    if local_vars:
        local_funcs_needed = set()
        local_funcs = {
            name: var
            for name, var in local_vars.items()
            if type(var) == type(lambda x: x)
        }

        for local_func in local_funcs:

            func_imported = False

            for import_names in imports:
                if local_func in import_names:
                    func_imported = True

            if func_imported or local_func in [func.__name__ for func in funcs]:
                continue

            for line in source:
                if f"{local_func}(" in line:
                    local_funcs_needed.add(local_func)

        if local_funcs_needed:
            assert (
                False
            ), f"Add the following local functions to `funcs` or set `local_vars` to `None`: {local_funcs_needed}"

    with open(fname, "w") as f:
        f.writelines(sorted(imports_needed))
        f.write("\n")
        f.writelines(source)
