import logging

import uvicorn


def main() -> int:
    uvicorn.run(
        "app.api.init_api:asgi_app",
        reload=True,
        log_level=logging.WARNING,
        server_header=False,
        date_header=False,
        port=8080,
    )

    return 0


if __name__ == "__main__":
    raise exit(main())
