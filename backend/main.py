from fastapi import FastAPI
from api.v1.routers import files
from fastapi.responses import RedirectResponse
# from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="bunch of llamas Docs",
    description="This documentation summarizes the bunch of llamas API.",
    version="0.0.1",
    contact={
        "name": "Jakob Zacherl",
        "email": "jakob@bunch.capital",
    }
)

app.include_router(files.router, prefix="/v1/files", tags=["files"])

# doesn't work for some reason
@app.get("/docs", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/redoc")


original_openapi = app.openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = original_openapi()
    openapi_schema["info"]["x-logo"] = {"url": "https://assets-global.website-files.com/61955627879747fa5333c3cd/637823ba8c7bd89dd2c35e26_bunch-logo-dark_146px.svg"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# # To set up a custom ReDoc documentation
# # Serve static files
# app.mount("/static", StaticFiles(directory="app/docs"), name="static")

# @app.get("/docs", include_in_schema=False)
# async def custom_redoc():
#     with open('custom_redoc.html', 'r') as html_file:
#         return HTMLResponse(content=html_file.read())