'''
Click command function 'edit'.
'''

import subprocess

import click

from posce.comms.base import group
from posce            import tools

@group.command(short_help='Edit note.')
@click.argument('name')
@click.option('-e', '--editor',
    help    = 'Editor program to use.',
    metavar = 'PROG',
    type    = str,
)
@click.pass_obj
def edit(book, name, editor):
    '''
    Open note NAME in editor.
    '''

    note = tools.clui.disambiguate(book, name)
    args = [editor, note.path] if editor else [note.path]
    subprocess.run(args, shell=True)
