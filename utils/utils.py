import sqlite3
from datetime import datetime

def to_list_of_dict(list: list) -> list:
    """
    Takes as parameter a list of sqlite3.Row Object and returns a corrispondent list of mutable dictionary

    :param row: the list of row object to be converted
    """

    output = []
    for row in list:
        output.append(to_dict(row))
    return output


def to_dict(row: sqlite3.Row) -> dict:
    """
    Takes as parameter an sqlite3.Row Object and returns a corrispondent mutable dictionary

    :param row: the row object to be converted
    """

    data = dict(row) # Convert the sqlite3.Row object to a dictionary
    data = {key: data[key] for key in row.keys()} # Make the keys of the dictionary mutable
    return data

def add_days_ago(table: list) -> list:
    """
    Takes as parameter a list of podcasts as sqlite3.Rows and adds a column containing a string saying how many days/hours/minutes ago was the last episode of the podcast posted

    :param podcasts: the list of podcasts as rows 
    """

    new_table = []
    for row in table:
        row = to_dict(row)

        try:
            last_update = row['last_update']
            row['last_update'] = days_ago(last_update)
        except KeyError as ke:
            posted = row['timestamp']
            row['posted'] = days_ago(posted) 
        except Exception as e:
            pass

        new_table.append(row)
    return new_table

def days_ago(timestamp: str) -> str:
    """
    Takes a timestamp string and returns a string indicating how many days/hours/minutes ago the timestamp was.

    :param timestamp: the timestamp string in format '%Y-%m-%d %H:%M:%S'
    :return: the string indicating how many days/hours/minutes ago the timestamp was
    """

    # Parse the timestamp string to a datetime object
    date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    # Get the current date and time
    now = datetime.now()
    # Calculate the difference between the two dates
    difference = now - date_time_obj
    # Check the number of days ago
    if difference.days == 1:
        return f"{difference.days} giorno fa"
    elif difference.days != 0:
        return f"{difference.days} giorni fa"
    # Check the number of hours ago
    elif difference.seconds // 3600 == 1:
        return f"{difference.seconds // 3600} ora fa"
    elif difference.seconds // 3600 != 0:
        return f"{difference.seconds // 3600} ore fa"
    # Check the number of minutes ago
    elif difference.seconds // 60 == 1:
        return f"{difference.seconds // 60} minuto fa"
    elif difference.seconds // 60 == 0:
        return f"meno di 1 minuto fa"
    return f"{difference.seconds // 60} minuti fa"