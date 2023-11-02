import uvicorn

from app.configs.environment import get_config
from app.app import create_app


app = create_app()
env = get_config()

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=env.HOST_URL,
                port=env.HOST_PORT,
                reload=False)
