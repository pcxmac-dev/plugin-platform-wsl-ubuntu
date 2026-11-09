"""WSL Ubuntu for Liminal (the user, 2026-11-07: "the platform is the interface for the software/hardware
which facilitates the liminal framework"; "the scope of the plugin is setting up WSL/Ubuntu and supporting
docker for the platform"; "then create a gentoo and fedora plugin as well, same scope/function"): Ubuntu
in WSL 2 on this Windows PC, set up by the plugin (WSL itself, the distribution, systemd and the default
user, Docker inside, the engine started, the user in the docker group), and its engine offered to the
framework as the Docker instance `wsl-ubuntu` (liminal_libs.docker.instances). Everything is the library's
WslDistribution (liminal_libs.machines.wsl); this module says which distribution.

    python -m plugin_platform_wsl_ubuntu status | setup [STEP ...] | run -- COMMAND | instances
"""
from __future__ import annotations

import os

from liminal_libs.machines.wsl import WslDistribution, WslError

__version__ = "0.6.0"


def _read_text(url: str) -> str:
    import urllib.request

    with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 - the plugin's own url
        return r.read().decode("utf-8", "replace")


class WslUbuntuPlugin(WslDistribution):
    name = "wsl-ubuntu"
    ICON = "ubuntu"  # Ubuntu's circle of friends (liminal-libs 1.33.0's icons.js)
    title = "WSL Ubuntu"
    about = "Ubuntu in WSL 2 on this Windows PC, with Docker inside: the Linux the platform's containers run in"
    api = "2.1"
    order = 700
    distribution = "Liminal-Ubuntu"  # Liminal's own, beside the user's Ubuntu (never the user's)
    family = "apt"
    docker_repository = "https://download.docker.com/linux/ubuntu"  # Docker's own, as its documentation gives it
    install_name = "Ubuntu"  # from Microsoft's list, installed as Liminal-Ubuntu
    DISTRIBUTION_VAR = "WSL_UBUNTU_DISTRIBUTION"
    USER_VAR = "WSL_UBUNTU_USER"


MACHINE = WslUbuntuPlugin()
