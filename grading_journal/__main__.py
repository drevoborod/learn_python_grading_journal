import uvicorn

from grading_journal.server import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8882, log_level="debug")