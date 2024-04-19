# Моделирование работы шаговых двигателей

Это приложение предназначено для моделирования работы шаговых двигателей на основе заданных команд. Приложение позволяет визуализировать траектории движения двигателя для различных начальных условий и команд.

### Требования

- Python 3.6 или выше
- Библиотеки: tkinter, matplotlib, unittest

### Установка

1. Клонируйте репозиторий или скачайте исходный код приложения.
2. Убедитесь, что у вас установлены все необходимые библиотеки.

### Запуск

1. Откройте терминал и перейдите в директорию с исходным кодом приложения.
2. Запустите приложение, выполнив команду: `python main.py`
3. Откроется главное окно приложения, где вы можете ввести параметры команды для шагового двигателя (путь и скорость) и запустить моделирование.
4. После запуска моделирования откроется новое окно с графиками траектории движения для четырех различных начальных скоростей.

### Использование

1. В главном окне приложения введите значения пути (в шагах) и скорости (в шагах в секунду) для команды шагового двигателя.
2. Нажмите кнопку "Запустить" для начала моделирования.
3. В новом окне будут отображены четыре графика, представляющие траектории движения двигателя для следующих начальных условий:
   - Разгон (начальная скорость 0)
   - Движение с постоянной скоростью (начальная скорость равна целевой скорости)
   - Изменение скорости (начальная скорость 300)
   - Остановка (начальная скорость 200)

### Закрытие приложения

При закрытии приложения траектории движения шагового двигателя будут сохранены в файле `trajectories.pkl` в текущем рабочем каталоге. При следующем запуске приложения эти траектории будут загружены и отображены в окне графиков.

### Модуль gui.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stepper_motor import StepperMotor

class PlotWindow(tk.Toplevel):
    """
    Класс для создания окна с графиками траектории движения шагового двигателя.

    Атрибуты:
        axes (list): Список осей для отрисовки графиков.

    Методы:
        plot_trajectories(trajectories): Отрисовка графиков траектории движения.
    """

    def __init__(self, parent):
        """
        Инициализация экземпляра класса PlotWindow.

        Аргументы:
            parent (tk.Tk): Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Графики траектории движения")
        self.geometry("800x600")

        figure = Figure(figsize=(8, 6), dpi=100)
        self.axes = figure.subplots(2, 2)

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_trajectories(self, trajectories):
        """
        Отрисовка графиков траектории движения шагового двигателя.

        Аргументы:
            trajectories (list): Список траекторий движения.
        """
        for i, trajectory in enumerate(trajectories):
            ax = self.axes.flatten()[i]
            ax.clear()
            ax.plot(trajectory)
            ax.set_title(f"Команда {i + 1}")
            ax.set_xlabel("Время")
            ax.set_ylabel("Положение")

        self.axes[0][0].figure.canvas.draw()

class MainWindow(tk.Tk):
    """
    Класс для создания главного окна приложения.

    Атрибуты:
        motor (StepperMotor): Экземпляр класса StepperMotor для моделирования шагового двигателя.
        trajectories (list): Список траекторий движения шагового двигателя.
        plot_window (PlotWindow): Экземпляр класса PlotWindow для отображения графиков.

    Методы:
        on_closing(): Обработчик события закрытия приложения.
        start_simulation(): Запуск моделирования работы шагового двигателя.
    """

    def __init__(self, parent=None):
        """
        Инициализация экземпляра класса MainWindow.

        Аргументы:
            parent (tk.Tk, optional): Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Моделирование шагового двигателя")
        self.geometry("400x200")

        self.motor = StepperMotor()
        self.trajectories = []

        path_label = tk.Label(self, text="Путь:")
        path_label.grid(row=0, column=0)
        self.path_input = tk.Entry(self)
        self.path_input.grid(row=0, column=1)

        speed_label = tk.Label(self, text="Скорость:")
        speed_label.grid(row=1, column=0)
        self.speed_input = tk.Entry(self)
        self.speed_input.grid(row=1, column=1)

        start_button = tk.Button(self, text="Запустить", command=self.start_simulation)
        start_button.grid(row=2, column=0, columnspan=2)

        self.plot_window = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """
        Обработчик события закрытия приложения.
        Останавливает выполнение команды шагового двигателя, закрывает окно с графиками
        и сохраняет траектории движения в файл.
        """
        # Остановка выполнения команды шагового двигателя
        self.motor.stop_execution()

        # Закрытие окна с графиками, если оно открыто
        if self.plot_window and self.plot_window.winfo_exists():
            self.plot_window.destroy()

        # Сохранение данных траекторий движения
        if self.trajectories:
            save_path = os.path.join(os.getcwd(), "trajectories.pkl")
            with open(save_path, "wb") as file:
                pickle.dump(self.trajectories, file)

        # Закрытие главного окна приложения
        self.destroy()

    def start_simulation(self):
        """
        Запуск моделирования работы шагового двигателя.
        Получает траектории движения для четырех различных начальных скоростей,
        отображает графики траектории движения в отдельном окне.
        """
        path = int(self.path_input.get())
        speed = int(self.speed_input.get())

        trajectories = []
        initial_speeds = [0, speed, 3 * speed // 2, speed]
        for initial_speed in initial_speeds:
            self.motor.execute_command(path, speed, initial_speed)
            trajectory = self.motor.get_trajectory()
            trajectories.append(trajectory)

        self.trajectories = trajectories

        if not self.plot_window or not self.plot_window.winfo_exists():
            self.plot_window = PlotWindow(self)

        self.plot_window.plot_trajectories(trajectories)

### Модуль stepper_motor.py

import time
import threading
import queue

class StepperMotor:
    """
    Класс для моделирования работы шагового двигателя.

    Атрибуты:
        current_speed (int): Текущая скорость двигателя (шагов в секунду).
        target_speed (int): Целевая скорость двигателя (шагов в секунду).
        position (int): Текущее положение двигателя (в шагах).
        acceleration (int): Ускорение двигателя (шагов/с^2).
        deceleration (int): Замедление двигателя (шагов/с^2).
        running (bool): Флаг, указывающий, выполняется ли команда в данный момент.
        thread (threading.Thread): Поток для выполнения команды.
        trajectory_queue (queue.Queue): Очередь для хранения траектории движения.

    Методы:
        accelerate(target_speed, path): Разгон двигателя до целевой скорости.
        move(path, speed): Движение двигателя с постоянной скоростью.
        change_speed(target_speed, path): Изменение скорости двигателя.
        stop(path): Остановка двигателя.
        execute_command(path, speed, initial_speed): Выполнение команды для двигателя.
        _execute_command(path, speed, initial_speed): Внутренний метод для выполнения команды в отдельном потоке.
        stop_execution(): Остановка выполнения команды.
        get_trajectory(): Получение траектории движения из очереди.
    """

    def __init__(self):
        """
        Инициализация экземпляра класса StepperMotor.
        """
        self.current_speed = 0
        self.target_speed = 0
        self.position = 0
        self.acceleration = 100  # шагов/с^2
        self.deceleration = 100  # шагов/с^2
        self.running = False
        self.thread = None
        self.trajectory_queue = queue.Queue()

    def accelerate(self, target_speed, path):
        """
        Разгон двигателя до целевой скорости.

        Аргументы:
            target_speed (int): Целевая скорость двигателя (шагов в секунду).
            path (int): Путь, который должен пройти двигатель (в шагах).

        Возвращает:
            list: Траектория движения двигателя (список положений).
        """
        trajectory = []
        self.target_speed = target_speed
        self.current_speed = 0  # Начальная скорость равна 0

        # Разгон
        while self.current_speed < target_speed:
            self.position += self.current_speed
            trajectory.append(self.position)
            self.current_speed += self.acceleration
            time.sleep(0.01)

        # Движение с постоянной скоростью
        remaining_path = path - self.position
        steps_at_target_speed = remaining_path // target_speed
        for _ in range(steps_at_target_speed):
            self.position += target_speed
            trajectory.append(self.position)
            time.sleep(1 / target_speed)

        # Остаток пути
        remaining_steps = remaining_path % target_speed
        self.position += remaining_steps
        trajectory.append(self.position)

        return trajectory

    # Документация остальных методов класса StepperMotor

### Модуль logger.py

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

def log_in_thread(level, message):
    """
    Функция для помещения сообщения в очередь для логирования в потоке.

    Аргументы:
        level (int): Уровень логирования (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL).
        message (str): Сообщение для логирования.
    """
    log_queue.put((level, message))

def log_worker():
    """
    Функция для обработки логов из очереди.
    Извлекает сообщения из очереди и записывает соответствующие логи с помощью логгера.
    """
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

### Модуль tests.py

import unittest
from unittest.mock import patch, Mock
from stepper_motor import StepperMot
