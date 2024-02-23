from loguru import logger
import sys
from faker import Faker
import numpy as np
import pandas as pd


@logger.catch(level="ERROR")
def generate_fake_email() -> str:
    """ 
    Function to generate some fake emails.

    Returns:
        str: A fake email.
    """
    fake = Faker()
    faker = fake.email()

    return faker


@logger.catch(level="ERROR")
def generate_fake_df(num_rows: int) -> pd.DataFrame:
    """
    Function to generate a mocked DataFrame with pre defined columns and random values.

    The DataFrame consists in 6 columns:
        string_column: String that will vary in apple, banana and grape
        int_column: Int that varies from 1 to 100
        float_column: Int that varies from 1.0 to 100.0
        datetime_column: Datetime that goes from 2010-01-01' to '2024-12-31'
        email_column: String containing a fake email
            Example: johndoe@example.com

    Args:
        num_rows(int): An integer containing the number of rows of the DataFrame and its columns.

    Returns:
        pd.DataFrame: A pandas DataFrame with mocked values.
    """

    try:

        data = {}

        data['string_column'] = np.random.choice(
            ['apple', 'banana', 'grape'], size=num_rows)

        data['int_column'] = np.random.randint(1, 100, size=num_rows)

        data['float_column'] = np.random.uniform(1.0, 100.0, size=num_rows)

        data['datetime_column'] = pd.to_datetime(np.random.choice(
            pd.date_range('2010-01-01', '2024-12-31'), size=num_rows))

        data['email_column'] = [generate_fake_email()
                                for _ in range(num_rows)]

        logger.success(f"Function finalizada")

        return pd.DataFrame(data)

    except Exception as e:
        raise (e)


if __name__ == '__main__':

    logger.add(
        sys.stderr, level="WARNING", serialize=True, backtrace=True)

    np.random.seed(42)

    df = generate_fake_df(100)

    logger.success("Successfully terminated")
