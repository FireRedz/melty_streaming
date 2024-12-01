from typing import Any

from fastapi import APIRouter

from app.objects import memory as melty_memory

router = APIRouter()


@router.get("/state")
async def melty_state() -> dict[str, Any]:
    if not melty_memory.read(melty_memory.MELTY_HEADER, 1):
        if not melty_memory.look_for_melty():
            return {"waiting": True}

    current_state = {"waiting": False}

    # Read memory
    for state in melty_memory.get_memory_config()["stateInfo"]:
        current_state[state["key"]] = melty_memory.read(
            state["location"], state["size"]
        )

    return current_state
