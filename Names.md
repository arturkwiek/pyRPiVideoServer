# Hostname
Dwa miejsca, oba w plikach cloud-init, które już masz:

**Hostname** — w pliku `user-data`, linia `hostname: raspberrypi`. Zmień wartość na dowolną (np. `hostname: pi-wideo`).

**Nazwa użytkownika** — w pliku `user-data`, w sekcji `users:` linia `- name: mwd`. To samo imię podajesz potem przy logowaniu `ssh <nazwa>@<ip>`.

Teraz kluczowa część pytania — kiedy to działa:

Pliki cloud-init (`user-data`, `network-config`) są przetwarzane **tylko przy pierwszym uruchomieniu**. Cloud-init zapisuje sobie, że już się wykonał, i przy kolejnych bootach ignoruje te pliki. Czyli: edycja `user-data` na karcie po pierwszym starcie **nic nie zmieni** — użytkownik i hostname są już utworzone w systemie.

Ale to nie znaczy, że jesteś zablokowany. Na **działającym** systemie zmienisz oba ręcznie przez SSH:

```bash
# Zmiana hostname (od razu i na stałe)
sudo hostnamectl set-hostname pi-wideo

# Zmiana nazwy użytkownika jest bardziej złożona:
# nie da się przemianować konta, na którym jesteś zalogowany,
# więc robi się to przez tymczasowe konto albo roota.
```

W praktyce: **hostname zmienisz po pierwszym uruchomieniu bez problemu** (`hostnamectl`, jedna komenda). **Nazwę użytkownika lepiej ustawić od razu w `user-data`** — późniejsza zmiana wymaga przelogowania, zmiany nazwy konta (`usermod -l`), katalogu domowego (`usermod -d -m`) i grupy, co jest upierdliwe i łatwo coś zepsuć.

Wniosek: jeśli masz wątpliwości co do nazwy użytkownika — ustaw ją teraz poprawnie w `user-data` przed włożeniem karty. Jeśli chcesz tylko zmienić hostname, możesz to spokojnie zrobić później jedną komendą.

Jeśli naprawdę chcesz, żeby cloud-init przetworzył pliki **jeszcze raz** od zera (np. przy testach), można wyczyścić jego stan komendą `sudo cloud-init clean --logs` i zrestartować — wtedy ponownie zaaplikuje konfigurację z karty. Chcesz, żebym pokazał pełną, bezpieczną procedurę zmiany nazwy użytkownika przez SSH?

# User name
Nie da się przemianować konta, na którym jesteś aktualnie zalogowany — dlatego potrzebujesz drugiego konta (tymczasowego), z którego wykonasz zmianę. Oto bezpieczna procedura. Załóżmy, że zmieniasz `mwd` → `nowynick`.

**1. Zaloguj się jako `mwd` i utwórz tymczasowe konto admina:**

```bash
sudo adduser tempadmin            # ustaw jakieś hasło
sudo usermod -aG sudo tempadmin
```

**2. Wyloguj się i zaloguj jako `tempadmin`:**

```bash
exit
ssh tempadmin@<ip-pi>
```

**3. Upewnij się, że `mwd` nie ma żadnych działających procesów, i zmień konto:**

```bash
# sprawdź, czy nikt nie jest zalogowany jako mwd
who

# zmień nazwę logowania
sudo usermod -l nowynick mwd

# przenieś katalog domowy /home/mwd -> /home/nowynick
sudo usermod -d /home/nowynick -m nowynick

# zmień nazwę grupy głównej (jeśli nazywała się mwd)
sudo groupmod -n nowynick mwd
```

**4. Sprawdź, czy konto działa — zaloguj się jako `nowynick`:**

```bash
exit
ssh nowynick@<ip-pi>
# katalog domowy powinien być /home/nowynick, sudo powinno działać
id
sudo whoami     # powinno zwrócić: root
```

**5. Usuń konto tymczasowe:**

```bash
sudo deluser --remove-home tempadmin
```

Kilka uwag:

Hasło, klucze SSH i pliki przenoszą się razem z katalogiem domowym (`-m`), więc logowanie hasłem dalej działa. Jeśli kiedyś dodawałeś użytkownika `mwd` ręcznie do pliku w `/etc/sudoers.d/`, sprawdź `sudo ls /etc/sudoers.d/` i popraw nazwę w środku — ale przy naszej konfiguracji uprawnienia sudo idą przez grupę `sudo`, więc nic nie trzeba ruszać.

Jeśli przy `usermod` pojawi się błąd „user mwd is currently used by process", to znaczy, że gdzieś jeszcze działa proces tego użytkownika (np. druga sesja SSH albo serwer wideo) — zamknij go i powtórz.

Najprościej, żeby uniknąć całej tej operacji: jeśli jeszcze nie odpaliłeś Pi na poważnie, po prostu popraw `- name:` w pliku `user-data` na karcie i zrób pierwszy boot od nowa. Chcesz wariant przez konto tymczasowe (powyżej) czy przez reset cloud-init i ponowny pierwszy start?