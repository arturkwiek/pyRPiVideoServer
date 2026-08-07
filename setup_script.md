Przygotuję gotowy skrypt instalacyjny, który możesz uruchomić po zalogowaniu, plus omówienie. Pogrupowałem warstwy: system → multimedia/wideo → Python → AI → sieć.Skrypt `setup_env.sh` instaluje wszystko warstwami. Możesz go przesłać na Pi albo wkleić komendy ręcznie blok po bloku.

Jak go uruchomić na Pi (po zalogowaniu przez SSH):

```bash
# Wariant A: prześlij plik z komputera (uruchom na SWOIM komputerze)
scp setup_env.sh mwd@<adres-ip>:~

# Wariant B: utwórz na Pi i wklej zawartość
nano setup_env.sh   # wklej, zapisz Ctrl+O, wyjdź Ctrl+X

# Następnie na Pi:
chmod +x setup_env.sh
./setup_env.sh
```

Co dostajesz:

- **System + narzędzia dev:** kompilatory, cmake, git, Python z `venv`.
- **Wideo:** `ffmpeg`, `v4l-utils` (kamery USB), biblioteki kodeków, GStreamer, opcjonalnie `libcamera` dla kamery CSI Pi.
- **Python (w izolowanym środowisku `~/video-ai`):** `opencv-python-headless`, `numpy`, `pillow`, `pandas`, `matplotlib`.
- **AI (lekkie, na CPU ARM64):** `onnxruntime`, `scikit-learn`, `scikit-image`, TensorFlow Lite runtime. PyTorch i YOLO/Ultralytics są w skrypcie jako opcjonalne (zakomentowane) — są ciężkie na Pi 4.
- **Sieć:** `nmap`, `iperf3`, `dnsutils`, `net-tools` plus prosty firewall `ufw` z otwartym SSH.

Kilka rzeczy, o których warto wiedzieć:

Wybrałem `opencv-python-headless` (bez GUI) — właściwy dla serwera. Jeśli będziesz chciał podgląd w oknie przez `ssh -X`, zamień na zwykłe `opencv-python` (w skrypcie jest komentarz, jak to zrobić).

Środowisko jest w `~/video-ai`. Przed pracą zawsze aktywuj: `source ~/video-ai/bin/activate`. Żeby aktywowało się automatycznie po zalogowaniu, dopisz tę linię na końcu `~/.bashrc`.

Po instalacji sprawdź szybki test: `python3 -c "import cv2, numpy, onnxruntime; print(cv2.__version__)"`.

PyTorch i YOLO świadomie zostawiłem zakomentowane — na samym CPU Pi 4 detekcja w czasie rzeczywistym będzie wolna. Jeśli celujesz w detekcję obiektów na żywo, lepiej działają modele w formacie `.tflite`/ONNX, ewentualnie akcelerator Coral USB.

Chcesz, żebym dorzucił gotowy szkielet skryptu w Pythonie do analizy wideo (np. wczytanie pliku/strumienia, przetwarzanie klatek i zapis wyniku)?