"""WSL Ubuntu for Liminal (the user, 2026-11-07: "the platform is the interface for the software/hardware
which facilitates the liminal framework"; "the scope of the plugin is setting up WSL/Ubuntu and supporting
docker for the platform"; "then create a gentoo and fedora plugin as well, same scope/function"): Ubuntu
in WSL 2 on this Windows PC, set up by the plugin (WSL itself, the distribution, systemd and the default
user, Docker inside, the engine started, the user in the docker group), and its engine offered to the
framework as the Docker instance `wsl-ubuntu` (liminal_libs.docker.instances). Everything is the library's
WslDistribution (liminal_libs.machines.wsl); this module says which distribution.

What it attaches to (0.9.0, plugin API 2.2; the user, 2026-11-11: "each plugin should reflect the the API its attached
to, and present links that provide documentation"): wsl.exe, Ubuntu's APT, Docker Engine and the install's init
(systemd), each with the makers' pages, its parts and its calls (apis.py), drawn on the plugin's page; `api_facts` says
what the plugin kept of them while it ran.

    python -m plugin_platform_wsl_ubuntu status | setup [STEP ...] | run -- COMMAND | instances
"""
from __future__ import annotations

import os

from liminal_libs.machines.wsl import WslDistribution, WslError

from .apis import APIS, facts

__version__ = "0.9.0"


def _read_text(url: str) -> str:
    import urllib.request

    with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 - the plugin's own url
        return r.read().decode("utf-8", "replace")


class WslUbuntuPlugin(WslDistribution):
    name = "wsl-ubuntu"
    ICON = "ubuntu"  # Ubuntu's circle of friends (liminal-libs 1.33.0's icons.js)
    title = "WSL Ubuntu"
    about = "Ubuntu in WSL 2 on this Windows PC, with Docker inside: the Linux the platform's containers run in"
    api = "2.2"
    apis = APIS  # what it attaches to: wsl.exe, APT, Docker Engine, systemd (apis.py)
    order = 700
    distribution = "Liminal-Ubuntu"  # Liminal's own, beside the user's Ubuntu (never the user's)
    family = "apt"
    docker_repository = "https://download.docker.com/linux/ubuntu"  # Docker's own, as its documentation gives it
    install_name = "Ubuntu"  # from Microsoft's list, installed as Liminal-Ubuntu
    DISTRIBUTION_VAR = "WSL_UBUNTU_DISTRIBUTION"
    USER_VAR = "WSL_UBUNTU_USER"

    def api_facts(self) -> dict:
        """What it kept of its APIs while it ran, asking nothing: Microsoft's list as last read, Docker inside as last
        seen, the init the last services scan found."""
        return facts(self)


MACHINE = WslUbuntuPlugin()
