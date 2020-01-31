
from toolchains import Toolchain


Toolchain(
    'x64-linux-gcc',
    prefix='x86_64-linux-gnu-',
    CC='gcc', CXX='g++', LINK='g++',
)

Toolchain(
    'x64-linux-gcc-7',
    prefix='x86_64-linux-gnu-',
    CC='gcc-7', CXX='g++-7', LINK='g++-7',
)

Toolchain(
    'x64-linux-gcc-8',
    prefix='x86_64-linux-gnu-',
    CC='gcc-8', CXX='g++-8', LINK='g++-8',
)
