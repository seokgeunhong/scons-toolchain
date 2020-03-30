# re2c
from SCons.Script import Builder
from toolchains import Toolchain


Toolchain(
    're2c',
    BUILDERS={
        'Source':Builder(action='re2c -W $SOURCE -o $TARGET',
                         suffix='.c',
                         src_suffix='.re')
    }
)
