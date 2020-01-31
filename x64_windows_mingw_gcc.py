
from toolchains import Toolchain


Toolchain(
    'x64-windows-mingw-gcc',
    prefix='x86_64-w64-mingw32-',
    CC='gcc', CXX='g++', LINK='g++',
)
