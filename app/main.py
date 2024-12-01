import sys

import uvicorn
from fastapi import FastAPI


def make_web_server() -> FastAPI:
    web = FastAPI()
    return web


def main(argv: list[str]) -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
