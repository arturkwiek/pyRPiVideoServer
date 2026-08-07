#!/usr/bin/env bash
# ============================================================================
#  Konfiguracja srodowiska: wideo + AI + sieci na Ubuntu Server 24.04 (RPi 4)
#  Uruchom po pierwszym zalogowaniu przez SSH:
#     chmod +x setup_env.sh && ./setup_env.sh
#  Mozesz tez wykonywac sekcje recznie, blok po bloku.
# ============================================================================
set -e

# ----------------------------------------------------------------------------
# 1. AKTUALIZACJA SYSTEMU
# ----------------------------------------------------------------------------
sudo apt update && sudo apt full-upgrade -y

# ----------------------------------------------------------------------------
# 2. NARZEDZIA DEWELOPERSKIE / KOMPILACJA
# ----------------------------------------------------------------------------
sudo apt install -y \
    build-essential cmake pkg-config git wget curl unzip \
    python3 python3-pip python3-venv python3-dev \
    htop tmux nano

# ----------------------------------------------------------------------------
# 3. MULTIMEDIA / WIDEO (systemowe biblioteki i kodeki)
# ----------------------------------------------------------------------------
sudo apt install -y \
    ffmpeg v4l-utils \
    libavcodec-dev libavformat-dev libswscale-dev libavutil-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    libjpeg-dev libpng-dev libtiff-dev

# Obsluga kamery CSI (libcamera) - opcjonalnie, jesli uzywasz kamery Pi
sudo apt install -y libcamera-apps || true

# ----------------------------------------------------------------------------
# 4. SIEC / NARZEDZIA DIAGNOSTYCZNE
# ----------------------------------------------------------------------------
sudo apt install -y \
    net-tools nmap iperf3 dnsutils traceroute ufw

# Prosty firewall: pozwol na SSH (mozesz wlaczyc pozniej: sudo ufw enable)
sudo ufw allow OpenSSH

# ----------------------------------------------------------------------------
# 5. SRODOWISKO PYTHON (wirtualne, izolowane)
# ----------------------------------------------------------------------------
python3 -m venv ~/video-ai
source ~/video-ai/bin/activate
pip install --upgrade pip wheel setuptools

# ----------------------------------------------------------------------------
# 6. BIBLIOTEKI PYTHON: WIDEO + DANE
# ----------------------------------------------------------------------------
pip install \
    numpy \
    opencv-python-headless \
    pillow \
    imutils \
    matplotlib \
    pandas

# Uwaga: opencv-python-headless = OpenCV bez GUI (idealne na serwer).
# Jesli chcesz okna cv2.imshow przez X11 forwarding, uzyj zamiast tego:
#   pip install opencv-python

# ----------------------------------------------------------------------------
# 7. AI / UCZENIE MASZYNOWE (lekkie, dzialajace na CPU ARM64)
# ----------------------------------------------------------------------------
pip install \
    onnxruntime \
    scipy \
    scikit-learn \
    scikit-image

# TensorFlow Lite runtime (lekki, do inferencji modeli .tflite):
pip install ai-edge-litert || pip install tflite-runtime || true

# (Opcjonalnie, CIEZKIE) PyTorch CPU - duzo RAM i miejsca, dziala wolno na Pi:
#   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# (Opcjonalnie) YOLO / Ultralytics - detekcja obiektow:
#   pip install ultralytics

echo ""
echo "============================================================"
echo " GOTOWE. Aktywuj srodowisko poleceniem:"
echo "     source ~/video-ai/bin/activate"
echo " Sprawdz OpenCV:"
echo "     python3 -c 'import cv2; print(cv2.__version__)'"
echo "============================================================"
