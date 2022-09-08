import pickle

from IPython.core.magic import register_line_magic, needs_local_scope

@register_line_magic
@needs_local_scope
def save(line: str, local_ns) -> None:
    """
    Usage: %save obj [path]
    Default path is tmp.pkl.
    ".pkl" will be added to path if not already present
    """
    usage = "%save obj [path]"
    line = line.strip()
    if " " in line:
        try:
            obj, path = line.split(" ")
        except ValueError:
            raise ValueError(f"Error saving object! Usage: {usage}")
        if not path.endswith(".pkl"):
            path += ".pkl"
    else:
        obj = line
        path = "tmp.pkl"
    
    obj = local_ns[obj]
    with open(path, "wb") as f:
        pickle.dump(obj, f)

@register_line_magic
def load(line: str):
    """
    Usage: %load [path]
    Default path is tmp.pkl
    ".pkl" will be added to path if not already present
    """
    path = line.strip()
    if not path:
        path = "tmp.pkl"
    if not path.endswith(".pkl"):
        path += ".pkl"
    with open(path, "rb") as f:
        return pickle.load(f)
