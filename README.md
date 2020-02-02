# SConsToolchain 0.1.0.dev-3

**Under developement and not for distribution**

Toolchain definitions for SCons.

Tested on SCons 3.x.

Features:
---

  - Define toolchains, which defines tools and arguments to build.
  - Define options, which defines additional arguments to build.
  - Select toolchains and options at runtime via SCons arguments

Usage
---

First, include code below into you `SConstruct` file.

```python
# Toolchain registry
from toolchain import toolchains

# Predefined toolchains
import toolchain.x64_linux_gcc
import toolchain.x64_windows_msys_gcc

# Find a toolchain with SCons arguments
try:
    toolchain = toolchains.toolchain(**ARGUMENTS)
except Exception as e:
    exit(1)
```

Second, define `Environment` with toolchain, and use it when build.

```python
env = toolchain.Environment()

env.Library(..)
env.Program(..)
```

Finally, build with a _toolchain_ argument:

```bash
scons toolchain=<toolchain>[+<option>[+..]] <target>
```

All options following are combined as ordered,
and proper toolchain is selected, or fail if none found.

```bash
# gcc 8 for 64 bit linux, with debug option.
scons toolchain=x64-linux-gcc-8+debug <target>
```

Predefined toolchains:
---

### _gcc_ family

- _x64_linux_gcc.Toolchain(_`'x64-linux-gcc'`_)_: Current version of _gcc_ installed, for 64bit _Linux_
- _x64_linux_gcc.Toolchain(_`'x64-linux-gcc-7'`_)_: _gcc_ 7.x, for 64bit _Linux_.
- _x64_linux_gcc.Toolchain(_`'x64-linux-gcc-8'`_)_: _gcc_ 8.x, for 64bit _Linux_.
- _x64_windows_mingw_gcc.Toolchain(_`'x64-windows-mingw-gcc'`_)_: _mingw-gcc_, for 64bit _Windows_.
- _x64_windows_msys_gcc.Toolchain(_`'x64-windows-msys-gcc`_)_: _msys-gcc_, for 64bit _Windows_.

```python
env = toolchains.toolchain('x64-windows-mingw-gcc').Environment()
env.Program(...)
```

### _gcc_ options

- _gcc_options.Option(_`'gcc-debug'`_)_: Enabled by `'+debug'`. Adds `-g` option to compilers.
- _gcc_options.Option(_`'gcc-warning'`_)_: Enabled by `'+warnings'`. Adds bunch of warning options for _gcc_.

```python
env = toolchains.toolchain('x64-linux-gcc+debug+warnings').Environment()
env.Program(...)
```

### _re2c_ lexer

- _re2c.Toolchain(_`'re2c'`_)_: _re2c_ lexer. Reads `*.re` files and generate `*.c` codes. See <https://re2c.org/> for details.

Use `Source()` builder.

```python
env = toolchains.toolchain('re2c').Environment()
env.Source(source='lex.re')
```

## _def_ `toolchain`(*_keys_, toolchain=_keys_)

Find and return a `Toolchain` instance with _keys_. Either `toolchain`(_toolchain_=_keys_) or `toolchain`(*_keys_) may be used.

### _keys_

Strings, which are single keys or multiple keys partitioned with `+`, or iterables which contain strings, or another iterables of strings. See `Toolchain.Join`() for details.

```python
toolchain(toolchain='gcc+debug+warning')
toolchain(['gcc','debug','warning'], ..)
toolchain(['gcc',['debug','warning']], ..)
toolchain(toolchain=['gcc','debug+warning'], ..)
# Equals toolchain('gcc').Join('debug','warning')
```

## _class_ `Toolchain`(key, options=_{}_, env=_{}_, **_envargs_)

Define and register a toolchain.

### _key_

_key_ is a string not containing `+`.

### _options_

A dictionary whose each key is option name and value is option _key_ or _Option_ instance. Options not specified here is not allowed to join.

```python
Toolchain('gcc',options={'debug':'gcc-debug'})
```

### _env_, **_envargs_

_env_ is a dictionary, merged with _envargs_ keyword arguments, which defines environment variables used to create _SCons.Environment_.

## _def_ _Toolchain_.`Join`(_self_, *_names_, option=_names_):

Find options with _names_ and join them to _self_. Either `Join`(option=_names_) or `Join`(*_names_) may be used.

_names_ are strings, which are single or multiple names partitioned with `+`, or iterables which contain strings, or another iterables of strings.

When you join options to a toolchain;

- A new toolchain with concatenated _keys_ are created and registered.
- Environment variables are merged:
  - Strings are considered as lists of one element.
  - Lists are merged, while duplicated values are suppressed, with order not preserved.
  - Dictionaries are merged, by overriding duplicated keys. See `dict.update()` reference.

## _class_ `Option`(_key_, _env_=_{}_, **_envargs_)

See `Toolchain` for construction.
