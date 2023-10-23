"""Retrieve secrets and return a dictionary of them."""

import os
import json
import boto3

from padel_handler.utils.enum import AWS


class SecretManager(boto3.session.Session):
    ENV = os.environ.get("ENV", "dev")
    SECRET_NAME = f"padel-handler/{ENV}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_client()

    def create_client(self):
        self.custom_client = super().client(
            service_name="secretsmanager",
            region_name=AWS.REGION_NAME.value
        )

    def get_secrets(self) -> dict:
        """
        Get secrets from AWS secrets manager.

        Return value: `dict`.
        """
        return json.loads(
            self.custom_client.get_secret_value(
                SecretId=self.SECRET_NAME
            ).get("SecretString", "{}")
        )


# Secrets are by default retrieved from environment variable.
# If only one single variable is missing, this secrets will be replaced
# by Amazon Secrets Manager service value.
# This way developers can easily set up their own values without worrying
# about being able to connect to AWS.
# At the same time, on staging and production environments it will make sure
# that our secret variable are securely stored.
secrets = {
    "SECRET_KEY": os.environ.get("SECRET_KEY"),
    "DB_USER": os.environ.get("POSTGRES_USER"),
    "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "DB_HOST": os.environ.get("POSTGRES_HOST"),
    "DB_PORT": os.environ.get("POSTGRES_PORT"),
    "DB_NAME": os.environ.get("POSTGRES_DB")
}

if not all(secrets.values()):
    secrets = SecretManager().get_secrets()
