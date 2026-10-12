import logging

logger = logging.getLogger(__name__)

class ReportWriter:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'w', encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error("Ошибка при записи %s: %s: %s", self.filename, exc_type.__name__, exc_val)
        if self.file is not None:
            self.file.close()
            self.file = None
        return False

    def write_section(self, title: str, content: str | list | dict | int | tuple | set) -> None:
        match content:
            case str() | int():
                self.file.write(f"=== {title} ===\n  {content}\n\n")
            case list():
                self.file.write(f"=== {title} ===\n")
                for line in content:
                    self.file.write(f"  {line}\n")
                self.file.write('\n')
            case dict():
                self.file.write(f"=== {title} ===\n")
                for key, value in content.items():
                    self.file.write(f"  {key}: {value}\n")
                self.file.write('\n')
            case _:
                self.file.write(f"=== {title} ===\n  {content}\n\n")