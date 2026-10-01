'''import cv2
import time
from stream_reader import VideoStream
from analyzer import StreamAnalyzer


def main():
    # Заміни на свою адресу. Для тестування веб-камери вкажи 0.
    RTSP_URL = 0
    print("Ініціалізація підключення...")
    try:
        # Створюємо об'єкт потоку і одразу запускаємо його в окремому Thread
        stream = VideoStream(RTSP_URL).start()
    except Exception as e:
        print(f"Помилка: {e}")
        return

    # Ініціалізація аналізатора
    analyzer = StreamAnalyzer()

    print("Моніторинг розпочато. Натисніть 'q' для виходу.")

    while True:
        start_time = time.time()

        # Отримуємо найсвіжіший кадр з фонового потоку
        ret, frame = stream.read()

        if not ret or frame is None:
            print("Втрата кадру або обрив потоку. Очікування...")
            time.sleep(1)  # Невелика пауза перед наступною спробою
            continue

        # Робимо копію для безпечного відображення (щоб не модифікувати оригінал під час аналізу)
        display_frame = frame.copy()

        # Виконуємо аналіз
        alerts = analyzer.analyze(display_frame)

        # Візуалізація результатів аналізу (Alerts)
        y_offset = 40
        for alert in alerts:
            # Червоний для зависання, помаранчевий для розмиття
            color = (0, 0, 255) if "FROZEN" in alert else (0, 165, 255)
            cv2.putText(display_frame, f"WARNING: {alert}", (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            y_offset += 35

        # Підрахунок та візуалізація FPS
        process_time = time.time() - start_time
        fps = 1.0 / process_time if process_time > 0 else 0
        cv2.putText(display_frame, f"FPS: {fps:.1f}", (20, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Виведення результату на екран
        cv2.imshow('Real-Time RTSP Monitor', display_frame)

        # Вихід з програми
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Коректне завершення роботи
    print("Зупинка системи...")
    stream.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
'''
import cv2
import time
import logging
from stream_reader import VideoStream
from analyzer import StreamAnalyzer

# 1. Налаштування логування
logging.basicConfig(
    level=logging.INFO,  # Рівень логування (INFO, WARNING, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stream_monitor.log"),  # Пишемо у файл
        logging.StreamHandler()  # Паралельно виводимо в консоль
    ]
)


def main():
    RTSP_URL = 0

    logging.info("Ініціалізація підключення до потоку...")
    try:
        stream = VideoStream(RTSP_URL).start()
    except Exception as e:
        logging.error(f"Помилка підключення: {e}")
        return

    analyzer = StreamAnalyzer()

    logging.info("Моніторинг розпочато. Натисніть 'q' для виходу.")

    # Змінна для уникнення спаму в логах (щоб не писати "FROZEN" 30 разів на секунду)
    last_logged_alerts = set()

    while True:
        start_time = time.time()
        ret, frame = stream.read()

        if not ret or frame is None:
            logging.warning("Втрата кадру або обрив потоку. Очікування...")
            time.sleep(1)
            continue

        display_frame = frame.copy()
        current_alerts = set(analyzer.analyze(display_frame))

        # 2. Запис у лог лише нових або зниклих алертів (щоб не засмічувати файл)
        new_alerts = current_alerts - last_logged_alerts
        resolved_alerts = last_logged_alerts - current_alerts

        for alert in new_alerts:
            logging.warning(f"Виявлено проблему: {alert}")

        for alert in resolved_alerts:
            logging.info(f"Проблема вирішена: {alert} (потік стабілізувався)")

        last_logged_alerts = current_alerts

        # Візуалізація на екрані (залишається без змін)
        y_offset = 40
        for alert in current_alerts:
            color = (0, 0, 255) if "FROZEN" in alert else (0, 165, 255)
            cv2.putText(display_frame, f"WARNING: {alert}", (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            y_offset += 35

        process_time = time.time() - start_time
        fps = 1.0 / process_time if process_time > 0 else 0
        cv2.putText(display_frame, f"FPS: {fps:.1f}", (20, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow('Real-Time RTSP Monitor', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("Отримано сигнал на завершення роботи.")
            break

    logging.info("Зупинка системи...")
    stream.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()