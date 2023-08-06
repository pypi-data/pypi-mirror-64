import sys
from typing import Any, TextIO, Callable, List

__all__: List[str]
__version__: str

def echo(*objects: Any, sep: str = ' ', end: str = '', file: TextIO = sys.stdout, flush: bool = False,
         newline: bool = False, print_func: Callable = print, **print_kwargs: Any):
    ...
