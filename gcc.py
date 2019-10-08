# gcc options

from toolchains import Toolchain

Toolchain(
    'gcc-debug',
    tags=['gcc','debug'],
    env = {'CCFLAGS':'-g'}
)

Toolchain(
    'gcc-warning-4',
    tags=['gcc','warning-4'],
    env = {
        'CFLAGS':[
            '-W','-Wall','-Wextra','-pedantic',
            '-Wconversion','-Wsign-conversion','-Wshadow',
            '-Wlogical-op','-Wjump-misses-init','-Wmissing-include-dirs',
            '-Wcast-qual',
            '-Wbad-function-cast','-Wwrite-strings','-Wpacked',
            '-Wredundant-decls','-Wpointer-arith','-Wfloat-equal',
            '-Wnested-externs',
        ]
    }
)
