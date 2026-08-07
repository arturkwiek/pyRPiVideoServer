Oto kompletna lista krok po kroku, od wyjęcia karty z pudełka do zalogowania się przez SSH.

1. **Wyjmij kartę SD z pudełka** i włóż ją do czytnika kart w swoim komputerze (Windows). Jeśli karta jest nowa — nic więcej nie trzeba.

2. **Zainstaluj i otwórz Raspberry Pi Imager** (wersja 2.x lub nowsza). Pobierz z raspberrypi.com/software jeśli jeszcze nie masz.

3. **Wybierz urządzenie:** *Raspberry Pi 4*.

4. **Wybierz system:** *Other general-purpose OS → Ubuntu → Ubuntu Server (LTS, 64-bit)*.

5. **Wybierz nośnik:** Twoją kartę SD. Sprawdź dwa razy literę dysku — zapis skasuje całą kartę.

6. **Pomiń kreator ustawień** (gdyby wyskoczył pytaniem o customizację, wybierz „No"/„Edit Settings → bez zmian"). Dla Ubuntu i tak konfigurujemy ręcznie.

7. **Kliknij „Write"** i poczekaj na zapis + weryfikację. Po zakończeniu Imager może wysunąć kartę.

8. **Wyjmij i włóż kartę ponownie** do czytnika, żeby Windows zamontował partycję rozruchową o nazwie **`system-boot`** (FAT32, widoczna jak zwykły dysk).

9. **Skopiuj na partycję `system-boot` dwa pliki**, które przygotowałem (`network-config` i `user-data`), **nadpisując** istniejące pliki o tych samych nazwach. To ustawia Wi-Fi „S22", użytkownika `mwd` z hasłem `root` i włącza SSH.

10. **Sprawdź, że pliki się zapisały** — otwórz każdy w edytorze (np. Notepad++) i potwierdź, że treść jest taka jak powinna, bez zmiany nazw (mają być bez rozszerzenia).

11. **Bezpiecznie wysuń kartę** z Windows (ikona „Bezpieczne usuwanie sprzętu"), żeby nie uszkodzić plików.

12. **Włóż kartę do Raspberry Pi 4** (gniazdo od spodu płytki).

13. **Podłącz zasilanie** (USB-C). Monitor i klawiatura nie są potrzebne.

14. **Odczekaj 5–10 minut** — pierwszy boot konfiguruje system i łączy się z Wi-Fi. W tym czasie SSH jeszcze nie odpowiada, to normalne.

15. **Znajdź adres IP Pi:** zaloguj się do panelu routera i poszukaj urządzenia o nazwie `raspberrypi` na liście klientów. Alternatywnie spróbuj `ping raspberrypi.local` z komputera.

16. **Połącz się przez SSH** z komputera: `ssh mwd@<adres-ip>` (np. `ssh mwd@192.168.1.42`). Przy pierwszym połączeniu wpisz `yes`, by zaakceptować klucz.

17. **Wpisz hasło:** `root`. Jesteś w środku — masz uprawnienia sudo.

18. **(Zalecane) Zmień hasło** na silniejsze: `passwd`. Hasło „root" jest bardzo słabe.

Gdy będziesz zalogowany, mogę podać komendy instalacji Pythona + OpenCV i szkielet skryptu do analizy wideo. Chcesz?