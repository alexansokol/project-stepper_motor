import unittest
from unittest.mock import patch, Mock
from stepper_motor import StepperMotor
from logger import logger, log_queue

class TestStepperMotor(unittest.TestCase):
    def setUp(self):
        self.motor = StepperMotor()

    @patch('stepper_motor.queue.Queue')
    def test_accelerate(self, mock_queue):
        trajectory = self.motor.accelerate(100, 1000)
        # Проверить правильность расчета траектории разгона
        self.assertIsInstance(trajectory, list)
        self.assertEqual(len(trajectory), mock_queue.put.call_count)

    @patch('stepper_motor.queue.Queue')
    def test_move(self, mock_queue):
        trajectory = self.motor.move(1000, 100)
        # Проверить правильность расчета траектории движения с постоянной скоростью
        self.assertIsInstance(trajectory, list)
        self.assertEqual(len(trajectory), mock_queue.put.call_count)

    @patch('stepper_motor.queue.Queue')
    def test_change_speed(self, mock_queue):
        trajectory = self.motor.change_speed(100, 1000)
        # Проверить правильность расчета траектории изменения скорости
        self.assertIsInstance(trajectory, list)
        self.assertEqual(len(trajectory), mock_queue.put.call_count)

    @patch('stepper_motor.queue.Queue')
    def test_stop(self, mock_queue):
        trajectory = self.motor.stop(1000)
        # Проверить правильность расчета траектории остановки
        self.assertIsInstance(trajectory, list)
        self.assertEqual(len(trajectory), mock_queue.put.call_count)

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.mock_queue = Mock()
        log_queue.put = self.mock_queue.put

    def tearDown(self):
        log_queue.put = log_queue.queue.put

    def test_log_levels(self):
        with self.assertLogs(logger, level='DEBUG') as cm:
            logger.debug('Отладочное сообщение')
            logger.info('Информационное сообщение')
            logger.warning('Предупреждение')
            logger.error('Ошибка')
            logger.critical('Критическая ошибка')

        self.assertEqual(len(cm.output), 5)
        self.assertIn('DEBUG:root:Отладочное сообщение', cm.output)
        self.assertIn('INFO:root:Информационное сообщение', cm.output)
        self.assertIn('WARNING:root:Предупреждение', cm.output)
        self.assertIn('ERROR:root:Ошибка', cm.output)
        self.assertIn('CRITICAL:root:Критическая ошибка', cm.output)
        self.assertEqual(self.mock_queue.put.call_count, 5)

if __name__ == '__main__':
    unittest.main()
