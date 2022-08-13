"""Process Handler, hooks onto Melty Blood and reads it's sweet succulent memory."""

import subprocess
import logging
import ctypes
from ctypes.wintypes import *
from typing import Optional

log = logging.getLogger(__name__)

# No idea what this stuff does, but it works.
STRLEN = 1
PROCESS_VM_READ = 0x0010

k32 = ctypes.WinDLL("kernel32")
k32.OpenProcess.argtypes = DWORD, BOOL, DWORD
k32.OpenProcess.restype = HANDLE
k32.ReadProcessMemory.argtypes = (
    HANDLE,
    LPVOID,
    LPVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
)
k32.ReadProcessMemory.restype = BOOL


def get_pid() -> Optional[int]:
    """Grabs the PID of the Melty Blood executable"""
    cmd = "tasklist"
    task_data = subprocess.check_output(cmd, creationflags=0x08000000).decode("UTF8")

    for proc in task_data.split("\n"):
        if proc.split(",")[0].startswith("MBAA"):
            return int(proc.split(",")[1])

    return None


PROCESS_ID = None
process = None


def look_for_melty() -> bool:
    """Looks for Melty Blood and sets the process"""
    global PROCESS_ID, process

    # Get Melty's PID
    PROCESS_ID = get_pid()

    if PROCESS_ID is not None:
        log.info("Melty Blood found! PID: " + str(PROCESS_ID))

        # Define the process.
        process = k32.OpenProcess(PROCESS_VM_READ, 0, PROCESS_ID)

        return True
    return False


def read(addr: int, size: int) -> Optional[int]:
    """Reads a part of memory from the process"""

    # Create a buffer.
    buf = ctypes.create_string_buffer(size)
    s = ctypes.c_size_t()

    if k32.ReadProcessMemory(process, addr, buf, size, ctypes.byref(s)):
        return int.from_bytes(buf.raw, "big")
    return None
