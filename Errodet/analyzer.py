import cv2
import numpy as np


class StreamAnalyzer:
    def __init__(self, frozen_threshold=500, frozen_limit=15, blur_threshold=39.0):
        self.frozen_threshold = frozen_threshold
        self.frozen_limit = frozen_limit
        self.blur_threshold = blur_threshold

        self.prev_frame = None
        self.frozen_frames_count = 0

    def analyze(self, frame):
        # Перетворюємо кадр у відтінки сірого для оптимізації обчислень
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        alerts = []

        # 1. Перевірка на зависання (Frozen stream)
        if self.prev_frame is not None:
            diff = cv2.absdiff(gray_frame, self.prev_frame)
            non_zero_count = np.count_nonzero(diff > 15)

            if non_zero_count < self.frozen_threshold:
                self.frozen_frames_count += 1
                if self.frozen_frames_count > self.frozen_limit:
                    alerts.append("FROZEN STREAM")
            else:
                self.frozen_frames_count = 0

        self.prev_frame = gray_frame

        # 2. Перевірка на розмиття (Blur)
        laplacian_var = cv2.Laplacian(gray_frame, cv2.CV_64F).var()
        if laplacian_var < self.blur_threshold:
            alerts.append(f"BLURRY (Var: {laplacian_var:.1f})")

        return alerts