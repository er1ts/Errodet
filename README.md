# Errodet
my course work about system of monitoring tool designed to detect visual defects and stability issues in network and local video feeds
Real-Time Video Stream Stability & Artifact Monitoring System

A lightweight, cross-platform Python monitoring tool designed to detect visual defects and stability issues in network and local video feeds (RTSP / UDP / UVC Webcams) in real time without buffering delay.

Developed as a Bachelor's qualification project at Igor Sikorsky Kyiv Polytechnic Institute (Faculty of Applied Mathematics, Department of System Programming and Specialized Computer Systems).

---

## ⚡ Key Features

- **Asynchronous Producer-Consumer Architecture**: Network frame polling runs in a dedicated background daemon thread (`VideoStream`), decoupling network I/O latency from the CPU-bound analytics pipeline. Old frames are atomically overwritten with zero buffer lag.
- **Artifact & Defect Detection**:
  - ❄️ **Frozen Stream Detection**: Evaluates frame-to-frame pixel-wise absolute difference ($\Delta(x, y) = |I_t(x, y) - I_{t-1}(x, y)|$) with thresholding to identify hardware freezes or network stalls.
  - 🔍 **Defocus & Blur Detection**: Computes the variance of the 2D Laplacian operator ($\sigma^2$) across high-frequency spatial gradients to detect blurred, dirty, or defocused lenses.
  - 🌑 **Exposure Anomalies**: Calculates the first-order mean brightness moment ($B_{\text{avg}}$) using NumPy vectorization to detect blackout/tampering (`TOO DARK`) or lens glare/sensor saturation (`OVEREXPOSED`).
- **State-Diff Smart Logging**: Deduplicates repetitive alerts using mathematical set differences (`current_alerts - last_logged_alerts`), logging only status transitions and recovery timestamps to `stream_monitor.log`.
- **Fault-Tolerant Auto-Recovery**: Intercepts device disconnects and timeouts gracefully by entering a low-power polling loop (1 Hz) and auto-restores normal operation in ~1.2s upon physical reconnection.
- **HUD & Telemetry**: Renders an on-screen display (OSD) showing active alerts, system status, and real-time processing FPS.

---

## 📊 Performance & Benchmarks

Validated on a 1080p (Full HD) @ 30 FPS video feed during a continuous 24-hour stability test:

| Test Metric | Experimental Result |
| :--- | :--- |
| **Throughput** | 55–62 FPS (2x compute margin over 30 FPS input) |
| **CPU Utilization** | 8–12% (single logical CPU core, zero GPU acceleration required) |
| **Memory Footprint** | Stable at ~42.0–43.5 MB RAM (0% memory leak detected) |
| **Freeze Detection Precision** | 99.0% |
| **Blur Detection Precision** | 97.0% |
| **Exposure Detection Precision** | 100.0% |

---

## 🛠 Tech Stack

- **Language:** Python 3.8+
- **Computer Vision & Processing:** OpenCV (`cv2`), NumPy
- **Concurrency:** Standard library `threading` (`Lock`, `Thread`)
- **Protocol & Hardware Support:** RTSP, UDP, V4L2 (Linux), DirectShow (Windows), AVFoundation (macOS)

---

## 📂 Project Structure

```text
video_monitoring_system/
├── config/
│   └── config.json          # Detection thresholds and stream configuration
├── src/
│   ├── __init__.py
│   ├── capture.py           # Thread-safe VideoStream class (Producer)
│   ├── analytics.py         # StreamAnalyzer analytical engine (Consumer)
│   └── main.py              # Application lifecycle, GUI overlay, and dispatcher
├── stream_monitor.log       # Persistent incident audit trail
├── requirements.txt         # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/video-monitoring-system.git
cd video-monitoring-system
```

### 2. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv

# On Linux / macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Configure your video source and detection thresholds in `config/config.json`:

```json
{
  "source": 0,
  "frozen_threshold": 22,
  "blur_threshold": 35.0,
  "dark_threshold": 30.0,
  "overexposure_threshold": 230.0
}
```

> **Tip:** Set `"source": 0` for your local USB webcam, or provide an RTSP URL string (e.g., `"rtsp://user:pass@192.168.1.100:554/stream1"`).

### 4. Run Monitoring

```bash
python src/main.py
```

- Press **`q`** inside the preview window to exit safely.
- Incident history is automatically recorded in `stream_monitor.log`.

---

## 👤 Author

- **Arsen Skibchyk** — Department of System Programming and Specialized Computer Systems, Igor Sikorsky Kyiv Polytechnic Institute.
