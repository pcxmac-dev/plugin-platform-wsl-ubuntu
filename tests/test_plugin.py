"""WSL Ubuntu: the distribution it names, its family, its variables, its engine as a Docker instance, all
through a stand-in wsl command (nothing runs here)."""
from __future__ import annotations

import pytest

from liminal_libs.machines.wsl import Wsl, WslError  # noqa: F401
from plugin_platform_wsl_ubuntu import MACHINE, WslUbuntuPlugin


def u16(text):
    return text.encode("utf-16-le")


class FakeWsl:
    def __init__(self, distributions=(), online=("Ubuntu", "FedoraLinux-42"), docker=False):
        self.distributions = list(distributions)
        self.online = list(online)
        self.docker = docker
        self.calls = []

    def __call__(self, args, timeout):
        self.calls.append(list(args))
        if args[1] == "--status":
            return 0, u16("Default Distribution: Ubuntu\r\nDefault Version: 2\r\n"), b""
        if args[1:3] == ["--list", "--verbose"]:
            return 0, u16("  NAME STATE VERSION\r\n" + "".join(f"  {n} {s} {v}\r\n" for n, s, v in self.distributions)), b""
        if args[1:3] == ["--list", "--online"]:
            return 0, u16("NAME FRIENDLY\r\n" + "".join(f"{n} x\r\n" for n in self.online)), b""
        if args[1] == "-d":
            command = args[args.index("--") + 1:]
            if command[:2] == ["docker", "--version"]:
                return (0, b"Docker version 28.1.1, build x\n", b"") if self.docker else (127, b"", b"not found")
            if command[:2] == ["docker", "info"]:
                return (0, b"28.1.1\n", b"") if self.docker else (1, b"", b"no daemon")
            return 0, (" ".join(command) + "\n").encode(), b""
        return 0, u16("ok"), b""


def test_the_plugin_names_its_distribution_and_offers_its_engine(monkeypatch):
    monkeypatch.delenv("WSL_UBUNTU_DISTRIBUTION", raising=False)
    monkeypatch.delenv("WSL_UBUNTU_USER", raising=False)
    assert MACHINE.name == "wsl-ubuntu" and MACHINE.family == "apt" and MACHINE.SYSTEM == "platform" and MACHINE.KIND == "machine"
    assert MACHINE.options == ("WSL_UBUNTU_DISTRIBUTION", "WSL_UBUNTU_USER") and MACHINE.user == "liminal"
    fake = FakeWsl(distributions=[("Ubuntu", "Running", "2")], docker=True)
    p = WslUbuntuPlugin(wsl=Wsl(runner=fake))
    assert p.present() and p.status()["engine"]["installed"] and p.status()["family"] == "apt"
    (inst,) = p.instances()
    assert inst.name == "wsl-ubuntu" and inst.command == f"wsl -d {p.distribution_name} docker" and inst.translate("C:\\\\x") == "/mnt/c/x"
    assert p.run("echo", "hi") == "echo hi\n"
    assert WslUbuntuPlugin(wsl=Wsl(runner=FakeWsl())).instances() == ()
