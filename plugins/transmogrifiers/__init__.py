import collections

import plugins
import lib.k8s
import lib.cmdline

from lib.decorators import classproperty

ArgExtra = collections.namedtuple('ArgExtra', ('flag', 'description', 'options', 'group'))
ArgExtra.__new__.__defaults__ = (dict(), None)  # options default to empty dict


class AbstractTransmogrifier(object):
    ''' The base class '''

    def __init__(self, args):
        self._args = args

    @classproperty
    def name(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @classproperty
    def description(cls):
        return cls.name

    @classproperty
    def deserialize_flag(cls):
        return False

    @classproperty
    def arggroup(cls):
        return cls.name

    @classproperty
    def argmeta(cls):
        return cls.name.upper()

    @classproperty
    def argextras(cls):
        return []

    def transmogrify(self, configs, output):
        ''' The main entry point of the class '''
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))


def execute(args):
    """ Executes all transmogrifiers specified """

    for subclass in AbstractTransmogrifier.__subclasses__():
        if hasattr(args, subclass.name) and getattr(args, subclass.name):
            subclass(args).transmogrify(
                lib.k8s.K8SConfigs(
                    args.configdir,
                    subclass.deserialize_flag),
                getattr(args, subclass.name)
            )


def __onload():
    plugins.import_att('plugins.transmogrifiers', __file__)

    for subclass in AbstractTransmogrifier.__subclasses__():
        lib.cmdline.add(
            subclass.arggroup,
            '--' + subclass.name,
            help=subclass.description,
            metavar=subclass.argmeta
        )

        for argextra in subclass.argextras:
            lib.cmdline.add(
                argextra.group or subclass.arggroup,
                '--' + subclass.name + '-' + argextra.flag,
                help=argextra.description,
                metavar=argextra.flag.upper(),
                **argextra.options
            )


__onload()

