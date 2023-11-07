from app.configs.database import init_engine
from app.models import (
    base_models,
    attachment_models,
    media_models,
    review_models,
    status_models,
    user_models
)


def init_db():
    base_models.Base.metadata.drop_all(bind=init_engine)
    base_models.Base.metadata.create_all(bind=init_engine)
