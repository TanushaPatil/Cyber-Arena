import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "cyber-arena-dev-secret-key"
    )