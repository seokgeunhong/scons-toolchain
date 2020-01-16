# SConsToolchain 0.1.0.dev-1

**Under developement and not for distribution**

Toolchain definitions for SCons.
Tested on SCons 3.x.

Features:
---

  - Define toolchains, which defines tools and arguments to build.
  - Select toolchains at runtime via SCons arguments
  - Combine toolchains at runtime via SCons arguments

Usage
---

First, include code below into you `SConstruct` file.

```python
# Toolchain registry
import toolchains

# Supported toolchains
import x64_linux_gcc
import x64_windows_mingw_gcc
import gcc_options

# Find a toolchain with SCons arguments
try:
    toolchain = toolchains.find(**ARGUMENTS)
    print('Found a toolchain.\n  ' + '\n  '.join(toolchain.log()))

except Exception as e:
    print('Error finding a toolchain: '+e.args[0])
    exit(1)
```

Second, define `Environment` with toolchain, and use it when build.

```python
env = Environment(ENV=os.environ, **toolchain.env())

env.Library(..)
env.Program(..)
```

Finally, build with a _toolchain_ argument:

scons `toolchain=`_id_[+_id_[+..]] _target_

All the toolchains specified are combined as ordered,
and proper toolchain is selected, or fail.

```bash
# Select gcc 8 for 64 bit linux, add gcc debug options and gcc warnings.
scons toolchain=x64-linux-gcc-8+gcc-debug+gcc-warnings <target>
```

Predefined toolchains:
---

### In `x64_linux_gcc`:

- `x64-linux-gcc`: Current version of gcc installed, for 64bit linux
- `x64-linux-gcc-7`: gcc 7.x, for 64bit linux.
- `x64-linux-gcc-8`: gcc 8.x, for 64bit linux.

### In `x64_windows_mingw_gcc`:

- `x64-windows-mingw-gcc`: mingw-gcc, for 64bit windows.

### In `x64_windows_msys_gcc`:

- `x64-windows-msys-gcc`: msys-gcc, for 64bit windows.

Predefined toolchain options:
---

### In `gcc_options`:

- `gcc-debug`: Add `-g` option.
- `gcc-warnings` Add bunch of warning options for _gcc_.

Defining a toolchain
---

Define a python2 module and write a Toolchain() per toolchain.

### _class_ `Toolchain`(`id`, `prefix`=_''_, `env`=_{}_)

#### `id`

`id` is a string or an iterable.

A string is a single id or multiple ids separated with `+`.

```python
Toolchain(id='x64-linux-gcc', ..)  # Key is ('x64-linux-gcc',)
Toolchain('x64-linux-gcc+gcc-debug', ..)  # Key is ('x64-linux-gcc','gcc-debug')
```

`id` may be an iterable, which yields another `id`s.

```python
Toolchain(['x64-linux-gcc','gcc-debug','gcc-warnings'], ..)
Toolchain(['x64-linux-gcc',['gcc-debug','gcc-warnings']], ..)
Toolchain(id=['x64-linux-gcc','gcc-debug+gcc-warnings'], ..)
# All three yield the same key: ('x64-linux-gcc','gcc-debug','gcc-warnings')
```

Each string is split with '+' into strings, nested iterables are flatten,
and all iterables are combined into a single tuple, or a _key_.

#### `prefix`

String prefixed to tool binaries.
Currently environment values of `CC`, `CXX`, and `LINK` are prefixed.

```python
# Compiler `x86_64-linux-gnu-gcc`, and linker `x86_64-linux-gnu-g++` is used.
Toolchain(.., prefix='x86_64-linux-gnu-', env={'CC':'gcc', 'LINK':'g++'})
```

When toolchains are combined, latter `prefix` overrides prior `prefix` if
not `None` or empty.

#### `env`

Dictionary of environment vairables.
Keys are strings, and values are single string, or list of strings.

When toolchains are combined, environment variables of same name are merged
supressing duplicated values. Also, order of values are ignored.

```python
Toolchain('gcc-debug', env={'CC':['-g','-W']})
Toolchain('gcc-warnings', env={'CC':['-W','-pedantic']})

find('x64-linux-gcc+gcc-debug')  # results env={'CC':['-W','-g','-pedantic']}
```
