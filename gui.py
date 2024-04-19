import tkinter as tk
import os
import pickle
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stepper_motor import StepperMotor

class PlotWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Графики траектории движения")
        self.geometry("800x600")

        figure = Figure(figsize=(8, 6), dpi=100)
        self.axes = figure.subplots(2, 2)

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_trajectories(self, trajectories):
        for i, trajectory in enumerate(trajectories):
            ax = self.axes.flatten()[i]
            ax.clear()
            ax.plot(trajectory)
            ax.set_title(f"Команда {i + 1}")
            ax.set_xlabel("Время")
            ax.set_ylabel("Положение")

        self.axes[0][0].figure.canvas.draw()

class MainWindow(tk.Tk):
    def __init__(self, parent=None):
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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
