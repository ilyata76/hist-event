from typing import NewType


Storage = NewType("Storage", str)


from .File import *
from .Range import *
from .Meta import *
from .Count import *