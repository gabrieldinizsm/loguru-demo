from loguru import logger
import sys
from faker import Faker


def generate_fake_email() -> str:
    """ 
    Function to generate some fake emails.

    Returns:
        str: A fake email.
    """
    fake = Faker()
    faker = fake.email()
    return faker
