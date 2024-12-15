"""Core module of dundie"""

from dundie.utils.log import get_logger

log = get_logger()


def load(filepath: str):
    """Loads data from filepath to the database

    Args:
        filepath (str): path to the employees file

    >>> len(load("assets/employees.csv"))
    2
    >>> load("assets/employees.csv")[0][:3]
    'Jim'
    >>> load("assets/employees.csv")[1][:6]
    'Dwight'
    """
    try:
        with open(filepath) as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as error_msg:
        log.error(str(error_msg))
        raise error_msg
