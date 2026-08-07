Zebrałem informacje. Kluczowy wniosek: dla **Ubuntu Server** zaawansowane ustawienia w Raspberry Pi Imager (Ctrl+Shift+X) działają zawodnie — Ubuntu konfiguruje się przez **cloud-init** (pliki `network-config` i `user-data` na partycji rozruchowej `system-boot`). To je trzeba edytować.

Przygotuję dwa gotowe pliki do skopiowania na kartę plus instrukcję.Najważniejsze: w **Ubuntu Server** konfiguracja Wi-Fi/SSH/użytkownika odbywa się przez **cloud-init**, a nie przez kreator Imagera. Po zaflashowaniu wyjmij i włóż kartę ponownie — pojawi się partycja **`system-boot`**. Tam podmieniasz dwa pliki (powyżej).

## TO DO

1. **Flashowanie:** w Raspberry Pi Imager wybierz urządzenie *Raspberry Pi 4* i system *Ubuntu Server (LTS, 64-bit)*. Użyj Imagera **2.x** (starsze nie obsługują cloud-init poprawnie).
2. **Pomiń kreator Imagera** (Ctrl+Shift+X) — dla Ubuntu te ustawienia i tak się nie zastosują. Po prostu zapisz obraz.
3. **Wyjmij i włóż kartę ponownie**, żeby system zamontował partycję `system-boot` (FAT32, widoczna w Windows).
4. **Skopiuj na partycję `system-boot`:**
   - `network-config` → ustawia Wi-Fi "S22" / hasło "java2015"
   - `user-data` → tworzy użytkownika **mwd** z hasłem **root**, włącza SSH i logowanie hasłem
   (nadpisz istniejące pliki o tych nazwach)
5. **Bezpiecznie odłącz kartę**, włóż do Pi, podłącz zasilanie.
6. **Czekaj 5–10 min** — pierwszy boot konfiguruje system, dopiero potem działa SSH.
7. **Znajdź adres IP** Pi w panelu routera (lista klientów) albo przez `ping raspberrypi.local`.
8. **Połącz się:** `ssh mwd@<adres-ip>` → hasło `root`. Przy pierwszym połączeniu zaakceptuj klucz (yes).

Logowanie sprawdzasz jako `mwd@…` z hasłem `root` (a nie „login root"). Po zalogowaniu masz uprawnienia sudo.

## Problemy i rozwiązania

**Ustawienia z kreatora Imagera nie działają** → To normalne dla Ubuntu — używaj plików cloud-init (`network-config`, `user-data`), nie kreatora.

**Pi nie pojawia się w sieci** → (a) Wi-Fi 5 GHz: RPi 4 obsługuje, ale upewnij się że "S22" nie jest tylko 6 GHz; (b) literówka w SSID/haśle — muszą być dokładnie w cudzysłowie; (c) odczekaj pełne 10 min.

**Błąd składni YAML (cloud-init po cichu pomija plik)** → tylko **spacje**, żadnych tabulatorów; `user-data` musi zaczynać się od `#cloud-config` w pierwszej linii, bez pustej linii ani BOM. Edytuj w Notepad++ / VS Code, nie w zwykłym Notatniku.

**`raspberrypi.local` nie odpowiada** → mDNS bywa zablokowany; znajdź IP w routerze i łącz się po adresie.

**SSH: "Connection refused" / "Permission denied"** → boot jeszcze trwa (poczekaj) albo `ssh_pwauth: true` nie zadziałało — sprawdź plik `user-data`. Logowanie hasłem jest celowo włączone w przygotowanym pliku.

**Złe partycje w Windows** → po flashowaniu Windows pokaże dwie partycje, edytowalna FAT32 to `system-boot`; drugiej (ext4) Windows nie widzi — to OK.

**Bezpieczeństwo** → hasło "root" jest bardzo słabe. Po pierwszym udanym logowaniu warto je zmienić (`passwd`) i docelowo przejść na klucz SSH.

Chcesz, żebym dodatkowo zapisał całość jako dokument (np. instrukcję `.md`)?

Sources:
- [How to install Ubuntu Server on your Raspberry Pi — Ubuntu](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi)
- [Install Ubuntu Server on Raspberry Pi in Headless Mode and SSH Into It — Linux Hint](https://linuxhint.com/install_ubuntu_ssh_headless_raspberry_pi_4/)
- [Headless Raspberry Pi Imaging Cloud-Init — pidiylab](https://pidiylab.com/headless-raspberry-pi-imaging-cloud-init/)
- [cloud-init WiFi na Raspberry Pi 4B / Ubuntu — GitHub martadinata666](https://github.com/martadinata666/cloud-init)