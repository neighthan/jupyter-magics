from typing import Any, Dict

from IPython import get_ipython
from IPython.core.magic import (
    Magics,
    line_magic,
    magics_class,
    needs_local_scope,
    no_var_expand,
)

try:
    import numpy as np
    import PIL
    import torch
    from jupyter_utils._visualize import Visualizer
    imports_ok = True
except ImportError:
    imports_ok = False

if imports_ok:
    @magics_class
    class Vis(Magics):
        def __init__(self, shell):
            super().__init__(shell)
            self.vis = None

        @line_magic
        @needs_local_scope
        @no_var_expand
        def img(self, line: str, local_ns=Dict[str, Any]) -> None:
            """
            %img [-c] img
            Use -c if you want to continue the previous visualization (i.e. overwrite the
            image there instead of creating a new image).
            """
            line = line.strip()
            if line.startswith("-c "):
                line = line[3:]
            else:
                self.vis = None

            self.shell.ex(f"_ = {line}")
            img = local_ns["_"]
            if isinstance(img, torch.Tensor):
                img = img.detach().cpu().numpy()
            elif isinstance(img, PIL.Image.Image):
                img = np.array(img)
            if not isinstance(img, np.ndarray):
                raise ValueError(f"Don't know how to handle image of type {type(img)}.")
            img = img.squeeze()
            if self.is_chw(img):
                img = img.transpose(1, 2, 0)
            if self.vis is None:
                # border=0 removes the right border, but the top one is still there...
                opts = dict(xaxis=None, yaxis=None, toolbar=None, border=0)
                if img.ndim == 2:
                    opts["cmap"] = "Greys_r"
                elif img.ndim != 3:
                    raise ValueError(
                        f"Don't know how to handle image with ndim = {img.ndim}; expected ndim = 2 or 3."
                    )
                self.vis = Visualizer(opts=opts)
            self.vis(img)

        @staticmethod
        def is_chw(img: np.ndarray) -> bool:
            return img.ndim == 3 and img.shape[0] == 3 and img.shape[2] != 3


    get_ipython().register_magics(Vis)
