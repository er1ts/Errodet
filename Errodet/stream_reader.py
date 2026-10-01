import cv2
import threading


class VideoStream:
    def __init__(self, src=0):
        # Ініціалізація підключення
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            raise Exception(f"Неможливо підключитися до джерела: {src}")

        # Зчитуємо перший кадр
        self.ret, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        # Запускаємо зчитування у фоновому потоці (daemon=True означає, що потік завершиться разом з основною програмою)
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        # Безперервний цикл зчитування кадрів
        while True:
            if self.stopped:
                self.stream.release()
                return

            # Читаємо наступний кадр з буфера
            self.ret, self.frame = self.stream.read()

    def read(self):
        # Повертає статус та останній зчитаний кадр
        return self.ret, self.frame

    def stop(self):
        # Сигнал для зупинки потоку
        self.stopped = True