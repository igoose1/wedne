import fastapi

from wedne.server.api import stats, visits

app = fastapi.FastAPI()
app.include_router(stats.router, prefix="/stats")
app.include_router(visits.router, prefix="/visits")
