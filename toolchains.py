

registry = {}


class NotFoundError(Exception):
    def __init__(self, **args):
        super(Exception, self).__init__('''`%s` not supported.

Supported toolchains are:
  %s''' % (
            ' '.join('%s=%s' % a for a in args.items()),
            '\n  '.join(sorted(str(t) for t in set(registry.values()))))
          )


def find(*toolchains, **args):

    keys = []

    for k in toolchains:
        keys += k.split('+') if isinstance(k,str) else k

    try:
        k = args['toolchain']
    except KeyError:
        pass
    else:
        keys += k.split('+') if isinstance(k,str) else k

    try:
        return registry[tuple(keys)]
    except KeyError:
        pass

    id = []
    tags = set()
    prefix = None
    env = {}

    for k in keys:
        try:
            t = registry[(k,)]
        except KeyError:
            raise NotFoundError(toolchain=(k,))

        id += t._id
        tags |= set(t._tags)  # union
        prefix = prefix if prefix else t._prefix  # replace only if none

        for k, v in t._env.items():
            a = env.get(k, set())
            b = t._env.get(k, set())
            a = {a} if isinstance(a, str) else set(a)
            b = {b} if isinstance(b, str) else set(b)
            env[k] = list(a|b)

    return Toolchain(id,tags=list(tags),prefix=prefix,env=env)


class Toolchain:

    def __init__(self,
                 id,
                 tags=[],
                 prefix='',
                 env={}):

        if not id:
            raise TypeError('Toolchain() parameter `id` is mandatory.')

        self._id = (id,) if isinstance(id, str) else tuple(id)
        self._tags = (tags,) if isinstance(tags, str) else tuple(tags)
        self._prefix = prefix
        self._env = env.copy()

        if registry.get(self._id, None):
            raise ValueError('Toolchain() id `%s` duplicated.' % str(self._id))
        else:
            registry[self._id] = self

    def __str__(self):
        return '+'.join(self._id)

    def log(self):
        return (
            'id=%s' % str(self),
            'tags=%s' % str(self.tags),
            'prefix="%s"' % str(self.prefix),
            'env=%s' % str(self.env()),
        )

    @property
    def id(self):
        return list(self._id)

    @property
    def tags(self):
        return list(self._tags)

    @property
    def prefix(self):
        return str(self._prefix)

    def env(self, key=None):
        if key is None:
            return { k : self._prefix_val(k,v) for k, v in self._env.items() }
        else:
            return self._prefix_val(key, self._env.get(key, None))

    def _prefix_val(self, key, val):
        if key in {'CC', 'CXX', 'LINK'}:
            v = val if isinstance(val,str) else '-'.join(val) 
            return str(self._prefix) + v if v else ''
        else:
            return val
