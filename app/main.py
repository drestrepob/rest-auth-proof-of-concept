from fastapi import FastAPI, HTTPException

from app.routers import api_key_router, basic_router, bearer_router

app = FastAPI(
    title='auth API',
    description='An API to test several authentification methods',
    version='0.1.0',
)

@app.get('/')
async def index():
    return {
        'message': 'Welcome to my server!'
    }

# Routers
app.include_router(api_key_router)
app.include_router(basic_router)
app.include_router(bearer_router)
