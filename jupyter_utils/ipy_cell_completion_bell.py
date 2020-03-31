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
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
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

    @magic_arguments()
    @argument(
        "-u",
        "--url",
        default="https://freewavesamples.com/files/E-Mu-Proteus-FX-CosmoBel-C3.wav",
        help="URL of audio file to play.",
    )
    @argument(
        "line_code",
        nargs="*",
        help="Other code on the line will be executed, unless this is called as a cell magic.",
    )
    @line_cell_magic
    def notify(self, line: str, cell: Optional[str] = None):
        args = parse_argstring(self.notify, line)

        code = cell if cell else " ".join(args.line_code)
        try:
            ret = self.shell.ex(code)
        finally:
            audio = _InvisibleAudio(url=args.url, autoplay=True)
            display(audio)

        return ret


get_ipython().register_magics(NotificationMagics)
