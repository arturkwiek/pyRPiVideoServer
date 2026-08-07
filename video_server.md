Zrobimy klasyczne headless podejście: Pi przechwytuje obraz z kamery i **wystawia go jako strumień MJPEG po HTTP**, który otworzysz w przeglądarce na dowolnym urządzeniu w sieci (`http://<ip-pi>:8000`). Tylko OpenCV + biblioteka standardowa, bez dodatkowych zależności.Gotowa „łapka". Przechwytuje obraz w wątku w tle i wystawia go na zewnątrz po HTTP — otwierasz w przeglądarce na laptopie/telefonie w tej samej sieci.

Jak uruchomić na Pi:

```bash
# 1. Otwórz port w firewallu
sudo ufw allow 8000

# 2. Prześlij plik z komputera (lub utwórz przez nano i wklej)
scp video_server.py mwd@<ip-pi>:~

# 3. Na Pi: aktywuj środowisko i uruchom
source ~/video-ai/bin/activate
python3 video_server.py
```

Potem na dowolnym urządzeniu w sieci otwórz `http://<ip-pi>:8000/` — zobaczysz podgląd na żywo. Dostępne ścieżki:

- `/` — strona z podglądem na żywo (strumień MJPEG)
- `/snapshot.jpg` — pojedyncza klatka (np. do pobrania przez `curl` albo skrypt)
- `/status` — prosty JSON do sprawdzenia, czy serwer żyje

Ważne rzeczy:

Domyślnie czyta kamerę USB z indeksu `0` (`/dev/video0`). Sprawdź, co masz, poleceniem `ls /dev/video*` oraz `v4l2-ctl --list-devices`. Jeśli kamera jest pod innym numerem, zmień `CAMERA_INDEX` u góry pliku.

Jeśli używasz **kamery CSI Pi** (taśmowej, nie USB), OpenCV jej domyślnie nie złapie przez `VideoCapture(0)` — wtedy najprościej podać pipeline GStreamer albo użyć `libcamera`. Powiedz, czy masz kamerę USB czy CSI, to dostosuję.

W metodzie `_loop` jest zaznaczone miejsce (komentarzem), gdzie wstawiasz **własną analizę wideo** — np. nakładanie czasu, detekcję ruchu czy obiektów. To samo, co wystawiasz, możesz tam przetwarzać.

To rozwiązanie jest do sieci lokalnej, bez szyfrowania i hasła. Nie wystawiaj portu 8000 wprost do internetu — jeśli chcesz dostęp z zewnątrz, zrób to przez SSH tunel albo VPN. Chcesz, żebym pokazał, jak uruchomić to jako usługę `systemd` (autostart po włączeniu Pi) albo dorzucił prostą detekcję ruchu?