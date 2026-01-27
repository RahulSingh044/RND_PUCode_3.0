from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routes import router

app = FastAPI(
    title="Incident Intelligence Service",
    version="1.0.0",
    description="AI service for detecting and scoring event incidents"
)

# API routes
app.include_router(router, prefix="/api", tags=["Incident Intelligence"])


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
