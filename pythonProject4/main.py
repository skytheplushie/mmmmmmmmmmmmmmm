from fastapi import FastAPI
from routers import task, user

app = FastAPI(swagger_ui_parameters=({"TryItOut Enabled":True}))


@app.get('/')
async def root():
    return {"message": "Welcome to Taskmanager"}


app.include_router(user.router)
app.include_router(task.router)