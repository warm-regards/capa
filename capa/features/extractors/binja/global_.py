import logging
import contextlib
from typing import Tuple, Iterator

from binaryninja import BinaryView

import capa.features.extractors.elf
from capa.features.common import OS, OS_MACOS, ARCH_I386, ARCH_AMD64, OS_WINDOWS, Arch, Feature
from capa.features.address import NO_ADDRESS, Address

logger = logging.getLogger(__name__)


def extract_os(bv: BinaryView) -> Iterator[Tuple[Feature, Address]]:
    name = bv.platform.name
    if "-" in name:
        name = name.split("-")[0]

    if name == "windows":
        yield OS(OS_WINDOWS), NO_ADDRESS

    elif name == "macos":
        yield OS(OS_MACOS), NO_ADDRESS

    elif name in ["linux", "freebsd", "decreee"]:
        yield OS(name), NO_ADDRESS

    else:
        # we likely end up here:
        #  1. handling shellcode, or
        #  2. handling a new file format (e.g. macho)
        #
        # for (1) we can't do much - its shellcode and all bets are off.
        # we could maybe accept a further CLI argument to specify the OS,
        # but i think this would be rarely used.
        # rules that rely on OS conditions will fail to match on shellcode.
        #
        # for (2), this logic will need to be updated as the format is implemented.
        logger.debug("unsupported file format: %s, will not guess OS", name)
        return


def extract_arch(bv: BinaryView) -> Iterator[Tuple[Feature, Address]]:
    arch = bv.arch.name
    if arch == "x86_64":
        yield Arch(ARCH_AMD64), NO_ADDRESS
    elif arch == "x86":
        yield Arch(ARCH_I386), NO_ADDRESS
    else:
        # we likely end up here:
        #  1. handling a new architecture (e.g. aarch64)
        #
        # for (1), this logic will need to be updated as the format is implemented.
        logger.debug("unsupported architecture: %s", arch)
        return
