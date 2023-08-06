from datetime import datetime


def wofy():
    now = datetime.now()
    year, wof, _ = now.isocalendar()
    return f"{year}-{wof}"
