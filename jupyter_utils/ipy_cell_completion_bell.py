"""
Adds a magic to IPython which will play a given sound when a cell finishes running.
Requires Python 3.6+.
Put this file in, e.g., ~/.ipython/profile_default/startup to load this magic on startup.

Usage:
```
%notify [-u/--url URL] [command]
```

Examples
```
%notify # no command needed
%notify run_long_command()
%notify -u https://www.example.com/sound.wav run_long_command()
```

There's also a cell magic version (don't put commands on the first line if using this).
```
%%notify [-u/--url URL]
command1()
command2()
...
```

To always play your preferred audio file, just change the default below.
"""

from IPython.display import Audio, display
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython import get_ipython
from typing import Optional


class _InvisibleAudio(Audio):
    """
    An invisible (`display: none`) `Audio` element which removes itself when finished playing.
    Taken from https://stackoverflow.com/a/50648266.
    """

    def _repr_html_(self) -> str:
        audio = super()._repr_html_()
        audio = audio.replace(
            "<audio", '<audio onended="this.parentNode.removeChild(this)"'
        )
        return f'<div style="display:none">{audio}</div>'


@magics_class
class NotificationMagics(Magics):
    """
    Inspired by https://stackoverflow.com/a/50648266.
    """

    @line_cell_magic
    def notify(self, line: str, cell: Optional[str] = None):
        splits = line.strip().split(" ")
        if splits[0] in ("-u", "--url"):
            url = splits[1]
            line = " ".join(splits[2:])
        else:
            url = "https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav"

        if cell:
            ret = self.shell.ex(cell)
        else:
            ret = self.shell.ex(line)

        audio = _InvisibleAudio(url=url, autoplay=True)
        display(audio)

        return ret


get_ipython().register_magics(NotificationMagics)
