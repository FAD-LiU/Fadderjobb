# STABENs Faddersystem

http://fadderjobb.staben.info/

## Bakgrund

Historiskt sett har det alltid varit svårt att planera fadderjobb för STABEN
eftersom det saknats ett sätt att delegera mindre jobb till faddrar. T.ex. har
det krävts faddrar som står i märkesbacken under första dagen, eller extra 
riggfaddrar till Hoben. Tanken med den här hemsidan är att underlätta detta arbete
genom att centralisera alla jobbpass till en hemsida som kan hantera alla pass
automatiskt.

## Deployment

Hemsidan är skriven i Django och konfigureras via följande environment-variabler:

* `DEBUG (False)`

    Default: `False`
    
    Bestämmer om Django ska köras i debug-läge.
    
* `DB_ENGINE`

    Default: `django.db.backends.postgresql_psycopg2`.
    
    Läs mer i
    [dokumentationen](https://docs.djangoproject.com/en/2.1/ref/databases/).

* `DB_NAME`

    Default: `fadderjobb`

* `DB_USER`

    Default: `fadderjobb`

* `DB_PASS`

    Default: `fadderjobb`

* `DB_HOST`

    Default: `localhost`

* `EMAIL_HOST`

    Default: `smtp.gmail.com`
    
* `EMAIL_PORT`

    Default: `587`

* `EMAIL_USER`

    Default: `None`

* `EMAIL_PASS`
    
    Default: `None`

## Funktionalitet

### Allmänt

_En användare kan:_

- Se vilka som är anmälda till vilka fadderjobb.
- Se en topplista över vilka faddrar som har tagit flest poäng.

### STABEN

_STABEN kan:_

- Skapa nya fadderjobb.
    - Beskrivning
    - Poäng
    - Antal faddrar som behövs
    - Typ av jobb
    - Länka till drive-dokument med mer info
- Stänga ett fadderjobb
    - Avanmälan kan endast ske om en annan fadder köar för platsen.
    - Finns lediga platser kan faddrar anmäla sig till dessa, trots att jobbet har stängt.

### Fadder

_En fadder kan:_

- Registrera sig på fadderjobb.
- Efter att anmälan har stängt:
    - Flagga för byte av registrerat jobb
- Flagga för önskan om specifikt jobb
    - Kösystem, den som är först i kön får jobbet.

## Planerat

### STABEN

_STABEN ska kunna:_

- Länka till drive-dokument med mer info
- Sätta en undre/övre gräns för mängd poäng

### Fadder

_En fadder ska kunna:_

- Vid utsatt tidpunkt innan nolle-p, få ett mail av STABEN med detaljerad
information angående de jobb som faddern har registrerat sig på.
