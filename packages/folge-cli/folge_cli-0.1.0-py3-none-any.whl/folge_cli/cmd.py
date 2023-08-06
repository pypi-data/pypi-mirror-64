import os
import platform
import subprocess
import sys
import typing

import click
import requests
from click_default_group import DefaultGroup

from . import __version__
from .documentation import upload_documentation

USER_AGENT = "Folge / %s" % __version__


def python_packages() -> typing.List[str]:
    """Return a list of python packages, formatted as package==version."""
    output = subprocess.check_output(["pip3", "freeze"])
    return [line.decode("utf-8") for line in output.splitlines()]


def platform_info() -> typing.List[str]:
    """Return a list of python packages, formatted as package==version."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
    }


def python_info() -> typing.List[str]:
    """Return a list of python packages, formatted as package==version."""
    return {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "packages": python_packages(),
        "path": sys.path,
    }


def collect():
    return {"platform": platform_info(), "python": python_info()}


@click.group(cls=DefaultGroup, default="run-program")
def main():
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--organization", type=str, required=True)
@click.option("--docs-key", type=str, required=True)
def upload_docs(organization, docs_key, path):
    upload_documentation(path, docs_key)


@main.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def run_program(args):
    url = os.environ.get("FOLGE_URL", "https://folge.io")
    app_id = os.environ.get("FOLGE_APP_ID")
    app_env = os.environ.get("FOLGE_ENVIRONMENT")
    app_version = os.environ.get("FOLGE_VERSION")

    if not args:
        click.echo("Please provide a program to run", err=True)
        sys.exit(1)

    if not app_version:
        click.echo(
            "[Folge] warning: no app_version, skipping data collection",
            err=True,
            color="red",
        )

    if app_id:
        click.echo("[Folge] submitting version information to %s" % url)
        data = collect()
        data["app_env"] = app_env
        data["app_version"] = app_version
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.post(
                "%s/api/application/%s/data" % (url, app_id), json=data, headers=headers
            )
            response.raise_for_status()
        except requests.RequestException:
            click.echo(
                "[Folge] warning: Failed to submit, HTTP code %d"
                % response.status_code,
                err=True,
                color="red",
            )
    else:
        click.echo(
            "[Folge] warning: no app_id specified, skipping data collection",
            err=True,
            color="red",
        )

    os.execvp(args[0], args)


if __name__ == "__main__":
    main()
