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
    """Return the full path of the jupyter notebook."""
    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'), params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)


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
        cells = json.loads(f.read())['cells']

    import_lines = []
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        source = cell['source']
        assert type(source) == list
        for line in source:
            line = line.strip()

            if line.startswith('#'):
                continue

            words = line.split(' ')

            if words[0] == 'import' or (words[0] == 'from' and words[2] == 'import'):
                import_lines.append(line)

    imported_names = []
    for line in import_lines:
        words = line.split(' ')
        if words[0] == 'import':  # ex import time or import numpy as np
            imported_names.append((words[-1],))
        else:  # ex from sklearn.metrics import roc_auc_score, roc_curve
            imported_names.append(tuple(word.replace(',', '') for word in words[words.index('import') + 1:]))

    return {imported_names[i]: import_lines[i] for i in range(len(imported_names))}
