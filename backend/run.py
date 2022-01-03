import os

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("SERVER_PORT", 9999)),
        log_level=os.getenv("LOG_LEVEL", "DEBUG").lower(),
        reload=True,
        reload_dirs=["src"],
    )
