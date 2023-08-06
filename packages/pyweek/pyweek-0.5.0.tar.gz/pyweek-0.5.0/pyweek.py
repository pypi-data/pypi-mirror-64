"""A command line interface to PyWeek.

Currently just a command for downloading the entries.

"""
import sys
import os
import re
from pathlib import Path
import time
from packaging import version

import requests
import click
import progressbar


__version__ = '0.5.0'
PYWEEK_URL = 'https://pyweek.org'
CLI_PYPI_URL = 'https://pypi.org/pypi/pyweek/json'


PROGRESSBAR_WIDGETS = [
    progressbar.Percentage(),
    ' ', progressbar.Bar(marker='\u2588'),
    ' ', progressbar.ETA(),
    ' ', progressbar.DataSize(),
]


sess = requests.Session()


def version_check():
    """Check that this CLI is up-to-date."""
    resp = sess.get(CLI_PYPI_URL)
    resp.raise_for_status()
    pkginfo = resp.json()
    v = version.parse(pkginfo['info']['version'])
    this_version = version.parse(__version__)
    if v > this_version:
        click.echo(
            click.style(
                f"There is a newer version {v} of this tool on PyPI. "
                "Please update before continuing:\n\n"
                "    pip install --upgrade pyweek",
                fg='red'
            )
        )
        sys.exit(1)


@click.group()
def cli():
    """Command line interface to PyWeek."""
    version_check()


def sanitise_name(name):
    """Strip name of characters that might be invalid in paths.

    >>> sanitise_name('What the Frog!?')
    'what-the-frog'

    """
    return re.sub(r'[^\w]+', '-', name.lower()).strip('-')


@cli.command()
@click.option(
    '-d', '--directory',
    type=Path,
    help="The directory to download into. " +
         "If omitted, download into a directory named after the challenge."
)
@click.argument(
    'challenge',
#    help="The challenge number to download entries for."
)
def download(challenge, directory):
    """Download all Pyweek entries for a competition."""
    if not directory:
        directory = Path.cwd() / str(challenge)

    directory.mkdir(parents=True, exist_ok=True)

    resp = sess.get(f'{PYWEEK_URL}/{challenge}/downloads.json')
    resp.raise_for_status()
    downloads = resp.json()

    errors = 0
    for name, files in downloads.items():
        entry_dir = directory / sanitise_name(name)
        entry_dir.mkdir(exist_ok=True)

        for f in files:
            name = f['name']
            url = f['url']
            size = f['size']
            target = entry_dir / name
            try:
                st = target.stat()
            except FileNotFoundError:
                pass
            else:
                if st.st_size == size:
                    # Already downloaded, skip
                    continue

            res = download_file(url, target, size)
            if not res:
                errors += 1

    if errors:
        click.echo(
            click.style(
                f"{errors} errors occurred while downloading files.",
                fg='red'
            )
        )
    else:
        click.echo(
            click.style(
                "All files downloaded successfully.",
                fg='green'
            )
        )


CHUNK_SIZE = 10240


def download_file(url, target, size):
    """Download the given file.

    Throttle to about the given rate in KB/s.

    """
    headers = {}
    if target.exists():
        start = target.stat().st_size
        headers['Range'] = f'bytes={start}-{size}'

    resp = sess.get(url, stream=True, headers=headers)
    if resp.status_code not in (200, 206):
        click.echo(
            click.style(
                f"Warning: error downloading {url}",
                fg='red'
            )
        )
        return False

    length = int(resp.headers['Content-Length'])

    name = f'{target.parent.name}{os.sep}{target.name}'

    if resp.status_code == 206:
        click.echo(
            "Resuming " + click.style(name, fg='cyan')
        )
        mode = 'ab'
    else:
        click.echo(
            "Downloading " + click.style(name, fg='cyan')
        )
        mode = 'wb'

    widgets = PROGRESSBAR_WIDGETS
    with progressbar.ProgressBar(widgets=widgets, max_value=size) as bar, \
            target.open(mode) as out:
        for chunk in resp.iter_content(102400):
            assert isinstance(chunk, bytes)
            out.write(chunk)
            bar.update(out.tell())
    return True


if __name__ == '__main__':
    cli()
