

'''Global toolchain registry'''
registry = {}


class WrongKeyError(Exception):
    '''Given key is not valid:

      - Id list is empty. i.e. None, '', or []
      - One or more id are empty. e.g. ['a','','c'], or 'a+b+'
    '''

    def __init__(self, key):
        super(Exception, self).__init__('Wrong toolchain id: `%s`' % str(key))

class NotFoundError(Exception):
    '''Faild to find a toolchain with given key'''

    def __init__(self, *toolchains, **args):
        super(Exception, self).__init__('''Not supported toolchain: `%s`

Supported toolchains are:
  %s''' % (
            '+'.join(_key(*toolchains, **args)),
            '\n  '.join(sorted(str(t) for t in set(registry.values()))))
          )

class DupKeyError(Exception):
    '''Toolchain already exists'''

    def __init__(self, *toolchains, **args):
        super(Exception, self).__init__('''Duplicated toolchain id: `%s`''' %
            ' '.join(_key(*toolchains, **args)))


def _key(*toolchains, **args):
    '''Get a new key, i.e. id list, with given arguments

    For argument details, see find().

      return  Id list.
      raise   WrongKeyError If any of id elements are in wrong format.
    '''

    key = []

    try:
        t = args['toolchain']  # toolchain=<key>
    except KeyError:
        pass
    else:
        key += _key(t)

    for t in toolchains:
        key += t.split('+') if isinstance(t, str) else _key(*t)

    if not key or [k for k in key if not k]:
        raise WrongKeyError(key)

    return key


def find(*toolchains, **args):
    '''Find a toolchain with given arguments

      toolchain=    A single string or an iterable.
      *toolchains   Single strings and/or iterables.

    Each string is a single id or multiple ids separated with `+`:

      find('x64-linux-gcc')  # Key is ('x64-linux-gcc',)
      find('x64-linux-gcc+gcc-debug')  # Key is ('x64-linux-gcc','gcc-debug')

    Each iterable yields another strings or iterables:

      find('x64-linux-gcc','gcc-debug','gcc-warnings')
      find(['x64-linux-gcc','gcc-debug','gcc-warnings'])
      find('x64-linux-gcc',['gcc-debug','gcc-warnings'])
      find(toolchain=['x64-linux-gcc','gcc-debug+gcc-warnings'])
      # All yield the same key: ('x64-linux-gcc','gcc-debug','gcc-warnings')

    Each string is split with '+' into strings, nested iterables are flatten,
    and all iterables are combined into a single tuple, or a _key_.

      return  Toolchain of _key_ if one is found in registry.
              If none found, define one by combining existing toolchains
              of each ids.
      raise   NotFoundError   If any of id is not found in registry.
              WrongKeyError   If any of id is in wrong format.
    '''

    key = _key(*toolchains, **args)
    try:
        return registry[tuple(key)]  # Cached
    except KeyError:
        pass

    # Combine
    id = []
    prefix = ''
    env = {}

    for k in key:
        try:
            t = registry[(k,)]
        except KeyError:
            raise NotFoundError((k,))

        id += t._id  # add
        prefix = prefix if prefix else t._prefix  # replace only if none

        for k, v in t._env.items():
            a = env.get(k, set())
            b = t._env.get(k, set())
            a = {a} if isinstance(a, str) else set(a)
            b = {b} if isinstance(b, str) else set(b)
            env[k] = list(a|b)

    return Toolchain(id,prefix=prefix,env=env)


class Toolchain:
    '''Define a toolchain'''

    def __init__(self, id, prefix='', env={}):
        '''
          id        A single string or an iterable. For details, see find().
          prefix    A string.
          env       Dictionary of environment variables.

          raise   WrongKeyError If any of id is in wrong format.
                  DupKeyError   If id exists found.
        '''

        self._id = tuple(_key(toolchain=id))
        self._prefix = prefix
        self._env = env.copy()

        try:
            registry[self._id]
        except KeyError:
            registry[self._id] = self
        else:
            raise DupKeyError(toolchain=self._id)

    def __str__(self):
        '''String form of id list, combined with '+'.
        
          e.g. 'x64_linux_gcc+gcc_debug'
        '''
        return '+'.join(self._id)

    def log(self):
        '''Log string tuple'''
        return (
            'id=%s' % str(self),
            'prefix="%s"' % str(self.prefix),
            'env=%s' % str(self.env()),
        )

    @property
    def id(self):
        '''Immutable iterable of ids

        e.g. ('x64_linux_gcc','gcc_debug')
        '''
        return self._id

    @property
    def prefix(self):
        '''Binary prefix'''
        return str(self._prefix)

    def env(self, key=None):
        '''Get environment variable

          return  Dictionary of all environment variables, if _key_ is None.
          return  Value of enviroment variable of given _key_.

        Values of variable ['CC', 'CXX', 'LINK'] are prefixed with `.prefix`.
        '''
        if key is None:
            return { k : self._prefixed(k,v) for k, v in self._env.items() }
        else:
            return self._prefixed(key, self._env.get(key, None))

    def _prefixed(self, key, val):
        if key in {'CC', 'CXX', 'LINK'}:
            v = val if isinstance(val,str) else '-'.join(val) 
            return str(self._prefix) + v if v else ''
        else:
            return val
