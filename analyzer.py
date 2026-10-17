import re
from datetime import datetime, date
from models import LogEntry
from decorators import timeit

class LogAnalyzer:
    def __init__(self, entry: list[LogEntry]):
        self.entry = entry

    def count_by_level(self) -> dict:
        count_dict = {}
        for x in self.entry:
            count_dict[x.level] = count_dict.get(x.level, 0) + 1
        return count_dict

    @timeit
    def unique_missing_classes(self) -> set:
        missing_classes = set()
        for x in self.entry:
            if x.missing_class is not None:
                missing_classes.add(x.missing_class)
        return missing_classes

    @timeit
    def unique_scripts_in_errors(self) -> set:
        script = re.compile(r"Script\s(\S+)")
        scripts = set()
        for x in self.entry:
            if x.level == "error":
                result_script = re.search(script, x.message)
                if result_script is not None and result_script not in scripts:
                    scripts.add(result_script.group(1))
        return scripts

    @timeit
    def top_errors(self, n: int = 10) -> list:
        top_errors_dict = {}
        for x in self.entry:
            top_errors_dict[x.message] = top_errors_dict.get(x.message, 0) + 1
        return sorted(top_errors_dict.items(), key=lambda kv: kv[1], reverse=True)[:n]

    @timeit
    def errors_per_minute(self) -> dict:
        errors_dict = {}
        for x in self.entry:
            if x.level in ("error", "missing"):
                errors_dict[x.timestamp.replace(second=0, microsecond=0)] = (
                        errors_dict.get(x.timestamp.replace(second=0, microsecond=0), 0) + 1)
        return errors_dict

    def filter_by_dates(self, date_from: date, date_to: date) -> list[LogEntry]:
        return list(filter(lambda x: date_from <= x.timestamp.date() <= date_to, self.entry))