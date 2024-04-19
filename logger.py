import logging
import threading
import queue

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Форматирование логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Очередь для логирования в потоке
log_queue = queue.Queue()

# Функция для логирования в потоке
def log_in_thread(level, message):
    log_queue.put((level, message))

# Функция для обработки логов из очереди
def log_worker():
    while True:
        try:
            level, message = log_queue.get(block=False)
            thread_logger = logging.getLogger(__name__)
            if level == logging.DEBUG:
                thread_logger.debug(message)
            elif level == logging.INFO:
                thread_logger.info(message)
            elif level == logging.WARNING:
                thread_logger.warning(message)
            elif level == logging.ERROR:
                thread_logger.error(message)
            elif level == logging.CRITICAL:
                thread_logger.critical(message)
        except queue.Empty:
            break

# Использование логгера
logger.debug('Отладочное сообщение')
logger.info('Информационное сообщение')
logger.warning('Предупреждение')
logger.error('Ошибка')
logger.critical('Критическая ошибка')

# Пример использования логгера в потоке
thread = threading.Thread(target=log_in_thread, args=(logging.INFO, 'Сообщение из потока'))
thread.start()

# Запуск потока для обработки логов из очереди
log_thread = threading.Thread(target=log_worker)
log_thread.daemon = True
log_thread.start()
