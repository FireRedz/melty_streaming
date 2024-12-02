from __future__ import annotations

import ctypes
import json
import logging
import subprocess
from ctypes.wintypes import *
from functools import cache
from pathlib import Path
from sys import platform
from typing import Optional

log = logging.getLogger(__name__)

# Read Windows API documentation
WIN_STRLEN = 1
WIN_PROCESS_VM_READ = 0x0010

MELTY_HEADER = 0x400000
MELTY_MEMORY_CONFIG = Path.cwd() / "app" / "ext" / "memory_config.json"

WIN_Kernel32 = ctypes.WinDLL("kernel32")
WIN_Kernel32.OpenProcess.argtypes = DWORD, BOOL, DWORD
WIN_Kernel32.OpenProcess.restype = HANDLE
WIN_Kernel32.ReadProcessMemory.argtypes = (
    HANDLE,
    LPVOID,
    LPVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
)
WIN_Kernel32.ReadProcessMemory.restype = BOOL

# Global Values
PROCESS_ID = None
process = None


@cache
def get_memory_config() -> dict[str, any]:
    if not MELTY_MEMORY_CONFIG.exists():
        raise RuntimeError("[Memory] MBAACC Memory Config missing!")

    return json.loads(MELTY_MEMORY_CONFIG.read_text())


def get_pid() -> int | None:
    """Grabs the PID of the Melty Blood executable"""
    cmd = "tasklist"
    task_data = subprocess.check_output(cmd, creationflags=0x08000000).decode("UTF8")

    for proc in task_data.split("\n"):
        if platform == "win32":  # windows tasklist
            if proc.startswith("MBAA.exe"):
                return int(list(filter(lambda x: len(x) >= 1, proc.split(" ")))[1])
        elif platform == "linux":  # wine tasklist
            if proc.split(",")[0].startswith("MBAA"):
                return int(proc.split(",")[1])

    return None


def look_for_melty() -> bool:
    """Looks for Melty Blood and sets the process"""
    global PROCESS_ID, process

    # Get Melty's PID
    PROCESS_ID = get_pid()

    if PROCESS_ID is not None:
        log.info("Melty Blood found! PID: " + str(PROCESS_ID))

        # Define the process.
        process = WIN_Kernel32.OpenProcess(WIN_PROCESS_VM_READ, 0, PROCESS_ID)

        return True
    return False


def read(addr: int, size: int) -> int | None:
    """Reads a part of memory from the process"""

    # Create a buffer.
    buf = ctypes.create_string_buffer(size)
    s = ctypes.c_size_t()

    if WIN_Kernel32.ReadProcessMemory(process, addr, buf, size, ctypes.byref(s)):
        return int.from_bytes(buf.raw, "big")
    return None
