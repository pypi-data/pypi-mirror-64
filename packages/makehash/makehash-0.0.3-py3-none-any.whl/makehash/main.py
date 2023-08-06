# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

import click
from click_anno import click_app
from click_anno.types import flag
from fsoopify import NodeInfo, NodeType, FileInfo, DirectoryInfo

EXTENSION_NAME = '.hash'

def get_checksum_file(f: FileInfo) -> FileInfo:
    return FileInfo(f.path + EXTENSION_NAME)

def verify_file(f: FileInfo):
    hash_file = get_checksum_file(f)
    hash_type = 'sha1'
    if not hash_file.is_file():
        if f.path.name.ext != EXTENSION_NAME:
            click.echo('Ignore {} by checksum file not found.'.format(
                click.style(str(f.path), fg='blue')
            ))
        return
    else:
        data = hash_file.load('json')
        hash_value = data[hash_type]
        click.echo('Verifing {}... '.format(
            click.style(str(f.path), fg='blue')
        ))
        click.echo('       - ', nl=False)
    real_hash_value, = f.get_file_hash(hash_type)
    if real_hash_value == hash_value:
        click.echo(click.style("Ok", fg="green") + '.')
    else:
        click.echo(click.style("Failed", fg="red") + '!')

def create_checksum_file(f: FileInfo, skip_exists: bool, skip_hash_file: bool):
    hash_file = get_checksum_file(f)

    if skip_hash_file and f.path.name.ext == EXTENSION_NAME:
        return

    if skip_exists and hash_file.is_file():
        return

    hash_type = 'sha1'
    click.echo('Computing checksum for {}... '.format(
            click.style(str(f.path), fg='bright_blue')
        ), nl=False)
    real_hash_value, = f.get_file_hash(hash_type)
    data = {}
    data[hash_type] = real_hash_value
    hash_file.dump(data, 'json')
    click.echo(click.style("Done.", fg="green"))

@click_app
class App:
    def _handle(self, handler, paths: list, **kwargs):
        def handle_dir(d: DirectoryInfo):
            for item in d.list_items():
                if item.node_type == NodeType.file:
                    handler(item, **kwargs)
                elif item.node_type == NodeType.dir:
                    handle_dir(item)

        if paths:
            for path in paths:
                node = NodeInfo.from_path(path)
                if node is not None:
                    if node.node_type == NodeType.file:
                        handle_file(node)
                    elif node.node_type == NodeType.dir:
                        handle_dir(node)
                else:
                    click.echo(f'Ignore {path} which is not a file or dir')
        else:
            click.echo(click.style("Path is required", fg="red"))

    def make(self, *paths, skip_exists: flag=True, skip_hash_file: flag=True):
        self._handle(create_checksum_file, paths,
            skip_exists=skip_exists,
            skip_hash_file=skip_hash_file)

    def verify(self, *paths):
        self._handle(verify_file, paths)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        App()(argv[1:])
    except Exception: # pylint: disable=W0703
        traceback.print_exc()

if __name__ == '__main__':
    main()
