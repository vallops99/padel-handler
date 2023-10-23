import os
import argparse
from dotenv import load_dotenv


load_dotenv()


def start_server():
    """Start uvicorn server."""
    os.system('uvicorn padel_handler.main:app --reload')


def generate_auto_revision():
    """
    Generate automatic Alembic revision.

    Use -m or --message parameter to add a revision message.
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-m",
        "--message",
        type=str
    )
    message = argparser.parse_args().message

    command = "alembic revision --autogenerate"
    command += f" -m '{message}'" if message else ""

    os.system(command)


def apply_revision():
    """
    Apply generated revisions
    """
    os.system("alembic upgrade head")
