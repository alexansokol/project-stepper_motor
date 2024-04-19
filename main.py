import tkinter as tk
import os
import pickle
from gui import MainWindow
from stepper_motor import StepperMotor
from logger import log_in_thread, logging

def main():
    root = tk.Tk()
    motor = StepperMotor()
    app = MainWindow(root, motor)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Загрузка предыдущих траекторий движения из файла (если есть)
    load_path = os.path.join(os.getcwd(), "trajectories.pkl")
    if os.path.exists(load_path):
        with open(load_path, "rb") as file:
            trajectories = pickle.load(file)
            app.trajectories = trajectories
            log_in_thread(logging.INFO, "Предыдущие траектории движения загружены из файла.")
    else:
        log_in_thread(logging.INFO, "Файл с траекториями движения не найден.")

    root.mainloop()

if __name__ == "__main__":
    main()
