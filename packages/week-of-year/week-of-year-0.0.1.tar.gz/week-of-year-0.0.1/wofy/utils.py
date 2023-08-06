from datetime import datetime


def wofy():
    now = datetime.now()
    return f"{now.year}-{now.month}"
