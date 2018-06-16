import argparse
import collections


__parser = argparse.ArgumentParser(
    description=(
        'Transmogrifier: Reads K8S configmaps and secrets '
        'and generates all kinds of useful things'
    ),
)

__parser.add_argument(
    'configdir', metavar='CONFIG_DIR',
    help='The directory to the k8s config files'
)

__parser_buffer = collections.defaultdict(list)


def add(group, flag, **kwargs):
    __parser_buffer[group].append([flag, kwargs])


def build():
    for group in sorted(__parser_buffer):
        group_parser = __parser.add_argument_group(group)

        for flag, kwargs in sorted(__parser_buffer[group], key=lambda item: item[0]):
            group_parser.add_argument(flag, **kwargs)


def parse():
    return __parser.parse_args()
