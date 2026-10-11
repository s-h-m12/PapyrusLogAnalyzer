import logging

logger = logging.getLogger(__name__)

class LogReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'r', encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error("Ошибка при чтении %s: %s: %s", self.filename, exc_type.__name__, exc_val)
        if self.file is not None:
            self.file.close()
            self.file = None
        return False

    def __iter__(self):
        if not self.file:
            raise RuntimeError("Файл должен быть открыт через контекстный менеджер")

        for line in self.file:
            yield line.rstrip("\r\n")
