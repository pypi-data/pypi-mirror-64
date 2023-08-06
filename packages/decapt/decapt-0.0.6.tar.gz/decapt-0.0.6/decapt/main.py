#!/usr/bin/env python
import argparse
import shlex
import subprocess
from subprocess import check_call, check_output, call
import re
import luxem
import os.path
import json
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
import abc
from functools import wraps


here = Path(__file__).parent
logging.basicConfig(level=logging.DEBUG)


def decolog(f):
    @wraps(f)
    def inner(*pargs, **kwargs):
        logging.debug(f"{f.__name__}: {repr(pargs)} {repr(kwargs)}")
        return f(*pargs, **kwargs)

    return inner


def lazy(f):
    f.lazied = ()

    @wraps(f)
    def inner(*pargs, **kwargs):
        if f.lazied:
            return f.lazied[0]
        f.lazied = (f(*pargs, **kwargs),)
        return f.lazied[0]

    return inner


class Sudo:
    def __init__(self):
        self.bg = subprocess.Popen(
            ["sudo", "python", here / "sudobg.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def _encode(self, o):
        if isinstance(o, dict):
            return {self._encode(k): self._encode(v) for k, v in o.items()}
        elif isinstance(o, (list, tuple)):
            return [self._encode(v) for v in o]
        elif isinstance(o, Path):
            return str(o)
        return o

    @decolog
    def _req(self, *pargs, **kwargs):
        self.bg.stdin.write(
            (json.dumps(self._encode([pargs, kwargs])) + "\n").encode("utf-8")
        )
        self.bg.stdin.flush()
        return json.loads(self.bg.stdout.readline())

    @decolog
    def c(self, *pargs, **kwargs):
        return self._req(*pargs, **kwargs)

    @decolog
    def cc(self, *pargs, **kwargs):
        ret = self._req(*pargs, **kwargs)
        print(ret["out"])
        if ret["code"] != 0:
            raise RuntimeError(ret["err"])

    @decolog
    def co(self, *pargs, **kwargs):
        ret = self._req(*pargs, **kwargs)
        if ret["code"] != 0:
            print(ret["out"])
            raise RuntimeError(ret["err"])
        return ret["out"]


@lazy
def sudo():
    return Sudo()


class Plugin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def id(self):
        pass

    @abc.abstractmethod
    def installed(self):
        pass

    @abc.abstractmethod
    def install(self, names):
        pass

    @abc.abstractmethod
    def uninstall(self, names):
        pass


DEFAULT_PLUGIN = "apt"


class APTPlugin(Plugin):
    def id(self):
        return "apt"

    def installed(self):
        return check_output(["apt-mark", "showmanual"]).decode("utf-8").splitlines()

    def install(self, names):
        manual = []
        default = []
        for name in names:
            if isinstance(name, dict):
                manual.append(name)
            else:
                default.append(name)
        sudo().cc(["apt-get", "install", "-y"] + default)
        for package in manual:
            p = Path(package["path"]).expanduser()
            check_call(["build.sh"], pwd=p)
            sudo().cc(["apt", "install", "-y", f'{package["name"]}.deb'], pwd=p)

    def uninstall(self, names):
        sudo().cc(["apt-mark", "auto"] + names)
        sudo().cc(["apt-get", "autoremove", "-y"])


class SnapPlugin(Plugin):
    def id(self):
        return "snap"

    def installed(self):
        return check_output(["snap", "list"])

    def install(self, names):
        for name in names:
            options = []
            if isinstance(name, dict):
                name = name["name"]
                options = name["options"]
            sudo().cc(["snap", "install", name] + options)

    def uninstall(self, names):
        sudo().cc(["snap", "remove"] + names)


PLUGINS = [
    APTPlugin,
    SnapPlugin,
]


def main():
    parser = argparse.ArgumentParser(
        description="Debianish Linux declarative package management"
    )
    parser.add_argument("conf", help="Configuration path", default="decapt.luxem")

    subparsers = parser.add_subparsers(title="Command", dest="_command")

    com_gen = subparsers.add_parser(
        "generate",
        description="Generate configuration from current explicitly installed packages",  # noqa
    )
    com_gen.add_argument(
        "-f", "--force", help="Overwrite existing configuration", action="store_true",
    )

    com_sync = subparsers.add_parser(
        "sync", description="Install, remove, and upgrade packages. Default command.",
    )
    com_sync.add_argument(
        "-n",
        "--dry-run",
        help="Show changes to be implemented on next sync",
        action="store_true",
    )

    args = parser.parse_args()

    plugins = [plugin() for plugin in PLUGINS]

    command = args._command
    if not command:
        command = "sync"

    if command == "generate":
        conf = dict(installed=[])
        for plugin in plugins:
            for package in plugin.installed():
                if plugin.id() == DEFAULT_PLUGIN:
                    conf["installed"].append(package)
                else:
                    conf["installed"].append(luxem.Typed(plugin.id(), package))
        if not args.force and os.path.exists(args.conf):
            print(f"{args.conf} already exists. Delete it or run with `-f`.")
            return
        with open(args.conf, "w") as out:
            luxem.dump(out, conf, pretty=True)

    elif command == "sync":
        with open(args.conf, "r") as conff:
            conf = luxem.load(conff)[0]
        installed = dict()
        add = dict()
        remove = dict()
        for package in conf["installed"]:
            if isinstance(package, luxem.Typed):
                plugin = package.name
                package = package.value
            else:
                plugin = DEFAULT_PLUGIN
            if isinstance(package, dict):
                package = package["name"]
            installed.setdefault(plugin, set()).add(package)
        for plugin in plugins:
            print(f"Scanning current package state for {plugin.id()}...")
            want = set(plugin.installed())
            add[plugin.id()] = want - installed.get(plugin.id(), set())
            remove[plugin.id()] = installed.get(plugin.id(), set()) - want

        if args.dry_run:
            print("\nPlan: Adding--\n{}".format(luxem.dumps(add)))
            print("\nPlan: Removing--\n{}".format(luxem.dumps(remove)))
        else:
            for plugin in plugins:
                print(f"Installing packages for {plugin.id()}...")
                plugin.install(add.get(plugin.id(), set()))
                print(f"Removing packages for {plugin.id()}...")
                plugin.remove(remove.get(plugin.id(), set()))

            if not add:
                print("No packages to install.")
            if not remove:
                print("No packages to remove.")

            print("Done")
