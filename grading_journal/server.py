from fastapi import FastAPI

from grading_journal.routers import router


app = FastAPI(title="Grading journal service", docs_url="/")
app.include_router(router)