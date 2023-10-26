import uvicorn

from app.configs.environment import get_environment_variables
from app.app import create_app


app = create_app()
env = get_environment_variables()

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=env.HOST_URL,
                port=env.HOST_PORT,
                reload=False)
