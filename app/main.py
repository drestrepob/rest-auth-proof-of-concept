from fastapi import FastAPI, HTTPException


app = FastAPI(
    title='auth API',
    description='An API to test several authentification methods',
    version='0.1.0',
)

@app.get("/")
def index():
    return {
        'message': 'Welcome to my server!'
    }
