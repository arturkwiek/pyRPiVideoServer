#!/usr/bin/env python3
# ============================================================================
#  video_server.py
#  Prosta "lapka": pobiera obraz z kamery i wystawia go na zewnatrz po HTTP.
#
#  - Strumien na zywo (MJPEG):   http://<ip-pi>:8000/
#  - Pojedyncza klatka (JPEG):   http://<ip-pi>:8000/snapshot.jpg
#  - Status (JSON):              http://<ip-pi>:8000/status
#
#  Uruchomienie (w aktywnym srodowisku ~/video-ai):
#     source ~/video-ai/bin/activate
#     python3 video_server.py
#
#  Wczesniej otworz port w firewallu:  sudo ufw allow 8000
# ============================================================================

import cv2
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ----------------------------- KONFIGURACJA --------------------------------
CAMERA_INDEX = 0        # 0 = pierwsza kamera (/dev/video0). USB webcam zwykle 0.
FRAME_WIDTH  = 640      # rozdzielczosc - mniejsza = plynniej na Pi
FRAME_HEIGHT = 480
JPEG_QUALITY = 80       # 1-100, kompromis jakosc / pasmo
HOST = "0.0.0.0"        # 0.0.0.0 = dostepne z calej sieci LAN
PORT = 8000
# ---------------------------------------------------------------------------


class Camera:
    """Watek przechwytujacy w tle, trzyma zawsze najnowsza klatke."""

    def __init__(self, index, width, height):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Nie mozna otworzyc kamery (index={index}). "
                "Sprawdz 'ls /dev/video*' oraz 'v4l2-ctl --list-devices'."
            )
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        while self.running:
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.05)
                continue
            # --- TU mozesz dodac wlasna analize wideo (detekcja, opisy itp.) ---
            # np. cv2.putText(frame, time.strftime("%H:%M:%S"), (10, 30),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            with self.lock:
                self.frame = frame

    def get_jpeg(self):
        with self.lock:
            if self.frame is None:
                return None
            ok, buf = cv2.imencode(
                ".jpg", self.frame,
                [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
            )
            return buf.tobytes() if ok else None

    def stop(self):
        self.running = False
        self.thread.join(timeout=1)
        self.cap.release()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # wycisz logi w konsoli

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._serve_page()
        elif self.path == "/stream.mjpg":
            self._serve_stream()
        elif self.path == "/snapshot.jpg":
            self._serve_snapshot()
        elif self.path == "/status":
            self._serve_status()
        else:
            self.send_error(404)

    def _serve_page(self):
        html = b"""<!doctype html><html><head><meta charset="utf-8">
        <title>Raspberry Pi - kamera</title>
        <style>body{font-family:sans-serif;background:#111;color:#eee;text-align:center}
        img{max-width:100%;height:auto;border:2px solid #444;margin-top:1rem}</style>
        </head><body><h2>Podglad na zywo</h2>
        <img src="/stream.mjpg"><p>Snapshot: <a style="color:#6cf"
        href="/snapshot.jpg">/snapshot.jpg</a></p></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def _serve_stream(self):
        self.send_response(200)
        self.send_header(
            "Content-Type",
            "multipart/x-mixed-replace; boundary=frame"
        )
        self.end_headers()
        try:
            while True:
                jpeg = camera.get_jpeg()
                if jpeg is None:
                    time.sleep(0.05)
                    continue
                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(
                    f"Content-Length: {len(jpeg)}\r\n\r\n".encode()
                )
                self.wfile.write(jpeg)
                self.wfile.write(b"\r\n")
                time.sleep(0.03)  # ~30 fps gorny limit
        except (BrokenPipeError, ConnectionResetError):
            pass  # klient zamknal karte - to normalne

    def _serve_snapshot(self):
        jpeg = camera.get_jpeg()
        if jpeg is None:
            self.send_error(503, "Brak klatki")
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(jpeg)))
        self.end_headers()
        self.wfile.write(jpeg)

    def _serve_status(self):
        body = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Otwieram kamere (index={CAMERA_INDEX})...")
    camera = Camera(CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serwer dziala. Otworz w przegladarce:  http://<ip-pi>:{PORT}/")
    print("Zatrzymanie: Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nZatrzymywanie...")
    finally:
        camera.stop()
        server.shutdown()
