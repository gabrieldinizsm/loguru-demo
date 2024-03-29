from loguru import logger
import sys
from faker import Faker
import numpy as np
import pandas as pd
import json
import time
import traceback
import platform
import psutil
from typing import Callable, Any


def log_function_info(log_env: bool = False, log_level: str = "WARNING") -> Callable:
    """
    Decorator to log some information about the execution of a function.

    Args:
        log_memory (bool): If True, log memory usage before and after function execution.

    Returns:
        Callable: Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        """
        Wrapper function for the decorator.

        Args:
            func(Callable): The target function to be decorated.

        Returns:
            Callable: Wrapper function.
        """
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Execute the decorated function, log relevant information, and handle exceptions.

            Args:
                *args(Any): Positional arguments passed to the target function.
                **kwargs(Any): Keyword arguments passed to the target function.

            Returns:
                Any: Result of the target function.
            """

            logger.add(sys.stdout, serialize=True, backtrace=True,
                       catch=True, level=log_level)

            start_time = time.time()
            initial_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            exception_info = None

            initial_memory = round(
                float(psutil.virtual_memory().used) / (1024.0 ** 2))

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                exception_info = {
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc()
                }
                raise e
            finally:
                end_time = time.time()
                final_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                elapsed_time = round(end_time - start_time, 4)

                final_memory = round(
                    float(psutil.virtual_memory().used) / (1024.0 ** 2))

                environment_info = {
                    "python_version": sys.version,
                    "operating_system": platform.system(),
                }

                log_data = {
                    "function_name": func.__name__,
                    "initial_timestamp": initial_timestamp,
                    "final_timestamp": final_timestamp,
                    "elapsed_time": elapsed_time,
                    "exceptions": exception_info,
                    "initial_memory_usage": initial_memory,
                    "final_memory_usage": final_memory
                }

                if log_env:
                    log_data["script_name"] = __file__
                    log_data["environment_info"] = environment_info

                logger.info(json.dumps(log_data, indent=4))

        return wrapper
    return decorator


@logger.catch('ERROR')
def generate_fake_email() -> str:
    """ 
    Function to generate some fake emails.

    Returns:
        str: A fake email.
    """
    fake = Faker()
    faker = fake.email()

    return faker


@log_function_info()
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

        return pd.DataFrame(data)

    except Exception as e:
        raise (e)


@log_function_info(log_env=True)
def main():

    np.random.seed(42)

    df = generate_fake_df(100)


if __name__ == '__main__':

    logger.info(
        f"""Initiating execution at {time.strftime('%Y-%m-%d %H:%M:%S')}""")

    main()

    logger.success(
        f"""Successfully terminated at {time.strftime('%Y-%m-%d %H:%M:%S')}""")
