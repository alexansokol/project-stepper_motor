import logging

# Настройка логирования
logging.basicConfig(filename='stepper_motor_simulator.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def log_simulation_start(path, speed, initial_speed):
    """Логирует начало симуляции"""
    logging.info(f"Starting simulation with path={path}, speed={speed}, initial_speed={initial_speed}")

def log_simulation_parameters(time, acceleration):
    """Логирует параметры симуляции"""
    logging.info(f"Simulation parameters: time={time:.2f}s, acceleration={acceleration:.2f} steps/s^2")
