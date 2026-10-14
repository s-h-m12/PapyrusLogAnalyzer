import re
import logging
from models import LogEntry
from datetime import datetime

DATE_PART = r"\d{2}/\d{2}/\d{4}"        # 10/10/2026
TIME_PART = r"\d{2}:\d{2}:\d{2}[AP]M"    # 05:39:58PM
ERROR_LEVEL_PATTERN = r"^Error:"
WARNING_LEVEL_PATTERN = r"^warning:"
MISSING_LEVEL_PATTERN = r"^Cannot open store for class"
CLASS_NAME_PATTERN = r"(?<=\")\w+(?=\")"
LOG_PATTERN = re.compile(rf"^\[(?P<date>{DATE_PART}) - (?P<time>{TIME_PART})\] (?P<message>.*)$")

logger = logging.getLogger(__name__)

# LogEntry = namedtuple("LogEntry", "timestamp level message missing_class")

# [10/10/2026 - 05:48:49PM] Error: Script QF_CH_Gwyndris_Dialogue_054AB2A0 cannot be bound
# to CH_Gwyndris_Dialogue (104AB2A0) because the script does not exist or is not currently loaded

# [10/10/2026 - 05:50:15PM] Cannot open store for class "PotionRackClickTriggerScript", missing file?

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
