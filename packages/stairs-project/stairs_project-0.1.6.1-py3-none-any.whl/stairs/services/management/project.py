import click
import os

from distutils.dir_util import copy_tree


@click.group()
def project_cli():
    pass


@project_cli.command('project:new')
@click.argument('name')
def make(name):
    """
    Makes a project, based on default template. It will contain all main
    stairs components and default app `core`.
    """

    default_project_path = os.path.join(_get_stairs_source_path(),
                                        'default/default_project')
    default_app_path = os.path.join(_get_stairs_source_path(),
                                    'default/default_app')

    path_to_user_project = './%s' % name
    copy_tree(default_project_path, path_to_user_project)
    copy_tree(default_app_path, os.path.join(path_to_user_project, 'core'))

    with open(os.path.join(path_to_user_project, 'config.py'), 'r') as config_f:
        config_body = config_f.read()

    with open(os.path.join(path_to_user_project, 'config.py'), 'w') as config_f:
        config_f.write(config_body)


# utils

def _get_stairs_source_path():
    default_project_path = __file__
    return os.path.dirname(os.path.dirname(os.path.dirname(default_project_path)))
