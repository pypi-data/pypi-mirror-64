#!/usr/bin/env python

#import plasmacli.component_manager as component_manager
#import plasmacli.workflow_manager as workflow_manager
#import plasmacli.project_manager as project_manager
#
from cometcli.utils import connect_comet, get_comet_status
from cometcli.file_manager import add_dataset, remove_dataset, list_datasets
import click
import os
import collections


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
def cli():
    pass


@click.command(name="status", help="get comet status")
def get_status():
    get_comet_status()


@click.argument('auth_key', required=True)
@click.command(name="connect", help="connect comet to space")
def connect(auth_key):
    connect_comet(auth_key)


@click.command(name="configure", help="configure comet settings")
def configure():
    # pass
    pass

# file command group


@click.group(cls=OrderedGroup, help="manage files on comet")
def file(name='file'):
    pass


@click.command(name="list", help="list files indexed on comet")
def list_files():
    list_datasets()


@click.command(name="add", help="add files to comet")
@click.argument('file_path', required=True)
def add_file(file_path):
    add_dataset(file_path)


@click.command(name="remove", help="remove file from comet")
@click.argument('file_path', required=True)
def remove_file(file_path):
    remove_dataset(file_path)


def build_cli():
    file.add_command(list_files)
    file.add_command(add_file)
    file.add_command(remove_file)
    cli.add_command(get_status)
    cli.add_command(connect)
    cli.add_command(configure)
    cli.add_command(file)
    return cli


def main():
    cli = build_cli()
    cli()


if __name__ == "__main__":
    main()
