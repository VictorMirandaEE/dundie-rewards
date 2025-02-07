"""Core module of dundie"""

from csv import reader

from dundie.database import add_employee, commit, connect
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath: str):
    """
    Load employee data from a CSV file, add employees to the database, and
      return a list of employee records.

    Args:
        filepath (str): The path to the CSV file containing employee data.

    Returns:
        list: A list of dictionaries, each containing employee data including
          name, department, role, email, points, and creation status.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    try:
        with open(filepath) as file:
            csv_data = reader(file)
            db = connect()
            employees = []
            headers = ["name", "department", "role", "email"]
            for row in csv_data:
                employee_data = dict(
                    zip(headers, [item.strip() for item in row])
                )
                email = employee_data.pop("email")
                employee_data, created = add_employee(db, email, employee_data)

                return_data = employee_data.copy()
                return_data["email"] = email
                return_data["points"] = db["balance"][email]
                return_data["created"] = created
                employees.append(return_data)

            commit(db)
            return employees

    except FileNotFoundError as error_msg:
        log.error(str(error_msg))
        raise error_msg
