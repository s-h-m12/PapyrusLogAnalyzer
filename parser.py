import re
import logging
from datetime import datetime

from models import LogEntry
from reader import LogReader

DATE_PART = r"\d{2}/\d{2}/\d{4}"        # 10/10/2026
TIME_PART = r"\d{2}:\d{2}:\d{2}[AP]M"    # 05:39:58PM
ERROR_LEVEL = "Error:"
WARNING_LEVEL = "warning:"
MISSING_LEVEL = "Cannot open store for class"
CLASS_NAME_PATTERN = r"(?<=\")\w+(?=\")"
LOG_PATTERN = re.compile(rf"^\[(?P<date>{DATE_PART}) - (?P<time>{TIME_PART})\] (?P<message>.*)$")

logger = logging.getLogger(__name__)

def parse_line(line) -> LogEntry | None:
    m = LOG_PATTERN.match(line)
    if not m:
        return None
    date = m.group("date")
    time = m.group("time")
    message = m.group("message")
    try:
        ts = datetime.strptime(f"{date} - {time}", "%d/%m/%Y - %I:%M:%S%p")
    except ValueError:
        logger.warning("Не удалось распарсить дату: %s - %s", date, time)
        return None
    level = "info"
    cl = None
    if message.startswith(ERROR_LEVEL):
        level = "error"
        return LogEntry(timestamp=ts, level=level, message=message, missing_class=None)
    elif message.startswith(WARNING_LEVEL):
        level = "warning"
        return LogEntry(timestamp=ts, level=level, message=message, missing_class=None)
    elif message.startswith(MISSING_LEVEL):
        level = "missing"
        try:
            cl = re.search(CLASS_NAME_PATTERN, message).group()
        except AttributeError:
            logger.warning("Не удалось распарсить название класса %s", message)
        return LogEntry(timestamp=ts, level=level, message=message, missing_class=cl)
    return LogEntry(timestamp=ts, level=level, message=message, missing_class=None)

def parse_file(path) -> list[LogEntry]:
    skipped = 0
    log = LogReader(filename=path)
    log_list = []
    with log as l:
        for line in l:
            entry = parse_line(line)
            if entry is not None:
                log_list.append(entry)
            else:
                skipped += 1
    logger.info("Разобрано %d записей, пропущено %d строк", len(log_list), skipped)
    return log_list