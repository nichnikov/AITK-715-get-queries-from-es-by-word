import logging

# 1. Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.INFO, # Уровень, с которого сообщения будут обрабатываться (INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Формат вывода сообщения
    datefmt='%Y-%m-%d %H:%M:%S' # Формат времени
)

# 2. Получаем объект логгера
# Использование __name__ — хорошая практика, так логгер будет называться именем модуля (например, 'my_script')
logger = logging.getLogger(__name__)