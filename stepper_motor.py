import time
import threading
import queue

class StepperMotor:
    def __init__(self):
        self.current_speed = 0
        self.target_speed = 0
        self.position = 0
        self.acceleration = 100  # шагов/с^2
        self.deceleration = 100  # шагов/с^2
        self.running = False
        self.thread = None
        self.trajectory_queue = queue.Queue()

    def accelerate(self, target_speed, path):
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

    def move(self, path, speed):
        trajectory = []
        self.target_speed = speed
        self.current_speed = speed  # Начальная скорость равна целевой скорости

        steps = path // speed
        for _ in range(steps):
            self.position += speed
            trajectory.append(self.position)
            time.sleep(1 / speed)

        remaining_steps = path % speed
        self.position += remaining_steps
        trajectory.append(self.position)

        return trajectory

    def change_speed(self, target_speed, path):
        trajectory = []
        self.target_speed = target_speed
        self.current_speed = 300  # Начальная скорость равна 300

        # Замедление
        while self.current_speed > target_speed:
            self.position += self.current_speed
            trajectory.append(self.position)
            self.current_speed -= self.deceleration
            time.sleep(0.01)

        # Движение с новой скоростью
        remaining_path = path - self.position
        steps_at_target_speed = remaining_path // target_speed
        for _ in range(steps_at_target_speed):
            self.position += target_speed
            trajectory.append(self.position)
            time.sleep(1 / target_speed)

        remaining_steps = remaining_path % target_speed
        self.position += remaining_steps
        trajectory.append(self.position)

        return trajectory

    def stop(self, path):
        trajectory = []
        self.target_speed = 0
        self.current_speed = 200  # Начальная скорость равна 200

        # Замедление
        while self.current_speed > 0:
            self.position += self.current_speed
            trajectory.append(self.position)
            self.current_speed -= self.deceleration
            time.sleep(0.01)

        # Остаток пути
        remaining_path = path - self.position
        self.position += remaining_path
        trajectory.append(self.position)

        return trajectory

    def execute_command(self, path, speed, initial_speed):
        self.running = True
        self.trajectory_queue = queue.Queue()
        self.thread = threading.Thread(target=self._execute_command, args=(path, speed, initial_speed))
        self.thread.start()

    def _execute_command(self, path, speed, initial_speed):
        if initial_speed == 0:
            trajectory = self.accelerate(speed, path)
        elif initial_speed == speed:
            trajectory = self.move(path, speed)
        elif initial_speed > speed:
            trajectory = self.change_speed(speed, path)
        else:
            trajectory = self.stop(path)

        # Отправка траектории движения в GUI через очередь
        for position in trajectory:
            self.trajectory_queue.put(position)

        self.running = False

    def stop_execution(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_trajectory(self):
        trajectory = []
        while not self.trajectory_queue.empty():
            trajectory.append(self.trajectory_queue.get())

        return trajectory
