# Fadderjobbsystemet

Ursprungligen skriven av Daniel Roos (STABEN Webb 18/19)

Vidareutvecklad av
- Emil Nilsson (STABEN Webb & Info 20/21)
- Joseph Hughes (STABEN Webb & Info 2022)
- Andreas Blomqvist (STABEN Webb & Info 2023 / FAD 2025)
- Oskar Arensmeier (STABEN Webb & Info 2024 / FAD 2025)

## Bakgrund

Historiskt sett har det alltid varit svårt att planera fadderjobb
eftersom det saknats ett sätt att delegera småjobb. T.ex. har det krävts faddrar
som står i märkesbacken under första dagen, eller extra riggfaddrar till Hoben.
Den här hemsidan försöker underlätta dessa problem genom att hantera anmälan,
byten, informationsutskick, m.m. automatiskt.

## Funktionalitet

### Allmänt

_En användare kan:_

- Se vilka som är anmälda till vilka fadderjobb.
- Se en topplista över vilka faddrar som har tagit flest poäng.

### Admin

_Admin:_

- Kan skapa nya fadderjobb.
    - Beskrivning
    - Poäng
    - Antal faddrar som behövs
    - Typ av jobb
- Kan stänga ett fadderjobb.
    - Avanmälan kan endast ske om en annan fadder köar för platsen.
    - Finns lediga platser kan faddrar anmäla sig till dessa, trots att jobbet har stängt.

### Fadder

_En fadder:_

- Kan registrera sig på fadderjobb.
- Kan om jobbet är fullt:
    - Ställa sig i kö till jobbet. Den som är först i kön när någon registrerad avregistrerar sig får jobbet.
- Kan efter att anmälan har stängt:
    - Flagga för önskan om avregistrering. Nästa person på tur kommer då få jobbet istället.
- Får mail när:
    - De har fått ett jobb som de köat för.
    - De har tappat ett jobb som de köat för att avanmäla sig till.
- Kan hämta en .ics-länk till en kalender för alla sina jobb.
- Byta jobb med andra faddrar

## Miljö

För att köra projektet krävs filen `.env` i root-mappen 
med följande struktur (sentry.io är valfritt):

```
DB_USER=stabenwebb
DB_PASSWORD=
EMAIL_USER=noreply@staben.info
EMAIL_PASSWORD=
SENTRYIO_DSN=
ADFS_CLIENT_ID=
```

Ytterligare konfiguration görs via följande environment-variabler:

* `DEBUG`

    Default: `False`
    
    Bestämmer om Django ska köras i debug-läge.
    
* `DB_ENGINE`

    Default: `django.db.backends.postgresql_psycopg2`.
    
    Läs mer i
    [dokumentationen](https://docs.djangoproject.com/en/2.1/ref/databases/).

* `DB_NAME`

    Default: `fadderjobb`

* `DB_HOST`

    Default: `localhost`

* `DB_PORT`

    Default: tom

* `EMAIL_HOST`

    Default: `smtp.gmail.com`
    
* `EMAIL_PORT`

    Default: `587`


### Development
Jag hade svårt att få igång Django i Windows. Därför rekommenderas Linux eller WSL.

Skapa ett virtual enviroment.
```shell
$ pip install virtualenv
$ virtualenv .venv
```

Aktivera miljon.
```shell
$ source .venv/bin/activate
```

Installera alla moduler.
```shell
$ pip install -r requirements.txt
```

## Körinstruktioner (lokalt)
Kommandot för python kan variera mellan `py`, `python3` eller `python`. Se till att du kör Python 3 och inte 2.

Kör alla databasmigrationer.
```shell
$ python3 manage.py migrate
```

Kör servern i dev mode.
```shell
$ python3 manage.py runserver
```

`manage.py` har en massa andra verktyg. För att lista tillgängliga kommandon, skriv:

```shell
$ python3 manage.py help
```

### Deployment (production)
Efter att ha committat något lokalt kör du följande för att få igång det på servern.

Anslut till servern och navigera till Fadderjobb-mappen.
```shell
$ ssh username@d-sektionen.lysator.liu.se
$ cd /srv/staben/Fadderjobb
```

Hämta dom senaste ändringarna.
```shell
$ git pull
```

Aktivera miljön.
```shell
$ source .venv/bin/activate
```

Om dina ändringar innehåller databasmigrationer, applicera dom.
```shell
$ python3 manage.py migrate
```

Starta om python-servern.
```shell
$ sudo systemctl restart uwsgi.service
```

## Databasmigrationer
För att uppdatera databasen efter att exempelvis ha redigerat `models.py` måste Django köra en databasmigrering.

Skapa en automatisk migration från kodändringarna.
```shell
$ python3 manage.py makemigrations
```

OBS: du bör inte köra `makemigrations` på servern eftersom dom skapade migrationerna bör vara i samma commit som kodändringarna.

Applicera nya migrationer. 
```shell
$ python3 manage.py migrate
```

Mer info om migrationer: https://docs.djangoproject.com/en/2.2/topics/migrations/

## Django-adminen
Admin-panelen nås via sidan /admin/.

Admin-konton skapas genom kommandot:

```shell
python3 manage.py createsuperuser
```

## Importera nya användare
Efter FU2:an kommer Fadderansvarig sannolikt ha ett stort excel-ark med alla faddrar. För att importera dessa finns ett enkelt skript i `accounts\management\commands\addrealusers.py`.

Detta körs på servern via
```shell
python3 manage.py addrealusers faddrar.csv --settings fadderjobb.settings_production
```

där faddrar.csv är en CSV fil utan rubriker med kolonnerna name, username, phone_number, email. Username bör vara faddrarnas LiU-id:n.
