
from toolchains import Toolchain


Toolchain(
    'x64-linux-gcc-8',
    tags=['x64-linux','gcc-8','gcc'],
    prefix='x86_64-linux-gnu-',
    env={
        'CC':'gcc-8',
        'CXX':'g++-8',
        'LINK':'g++-8',
    }
)
