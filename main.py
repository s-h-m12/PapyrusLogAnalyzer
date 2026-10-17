import logging
from datetime import datetime

from parser import parse_file
from analyzer import LogAnalyzer
from writer import ReportWriter

LOG_PATH = r"C:\Users\user\PycharmProjects\LogAnalyzer\sample.log"
SELF_PATH = r"C:\Users\user\PycharmProjects\LogAnalyzer\output.txt"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Начинаю разбор файла: %s", LOG_PATH)

    entries = parse_file(LOG_PATH)
    if not entries:
        logger.error("Не удалось разобрать лог или файл пуст. Завершаю работу.")
        return

    analysis = LogAnalyzer(entries)

    logger.info("Собираю статистику...")

    missing_classes = sorted(list(analysis.unique_missing_classes()))
    error_scripts = sorted(list(analysis.unique_scripts_in_errors()))

    sections = {
        "Всего записей": len(analysis.entry),
        "Распределение по уровням": analysis.count_by_level(),
        "Уникальные отсутствующие классы": missing_classes,
        "Уникальные скрипты в ошибках": error_scripts,
        "Топ-10 самых частых сообщений": analysis.top_errors(10),
        "Ошибки по минутам": analysis.errors_per_minute()
    }

    logger.info("Сохраняю отчет в файл: %s", SELF_PATH)
    with ReportWriter(SELF_PATH) as writer:
        for title, content in sections.items():
            writer.write_section(title, content)

    logger.info("Готово! Анализ завершен.")


if __name__ == "__main__":
    main()