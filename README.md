# Jupyter Utils

A few functions / magics for working with Jupyter notebooks.

## Usage

* The `%notify` / `%%notify` magic can be used to play a sound once a line or cell, respectively, finishes execution.
* The `%img` magic can be used to visualize images (and automatically handles things like converting PyTorch tensors). Use `%img -c` to update the previous image instead of creating a new plot (e.g. to visualize a sequence of observations from a reinforcement learning environment)

## Installation

```bash
pip install git+https://github.com/neighthan/jupyter-utils
```

Not to be confused with [`jupyter_utils`].

[`jupyter_utils`]: https://github.com/gsemet/jupyter_utils
