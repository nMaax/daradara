# DaraDara

DaraDara è una semplice applicazione web per l'ascolto e la pubblicazione di podcast.

Il nome deriva dall'onomatopea giapponese「だらだら」che, secondo [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), si usa per indicare il "vocio" che si crea quando una persona sta "parlando o spiegando qualcosa di molto poco chiaro e ci sta mettendo tantissimo tempo per farlo"

## Installazione veloce

Per avviare l'applicazioe è sufficente collocarsi nel percorso file opportuno e digitare i seguenti comandi sul proprio terminale

```prompt
pip install -r requirements.txt
flask run
```

Dopodichè sarà necessario aprirle una pagina web all'inidirizzo ```127.0.0.1:5000``` nel proprio browser preferito.

## Utenti e serie già presenti

DaraDara è già fornito di alcuni dati di esempio per fornire un esperienza utente basilare per testare tutte le feature messe a disposizione e richieste dal tema d'esame

### Utenti

In DaraDara ci sono già 6 utenti: **2 ascoltatori** e **4 creatori**

Ogni utente è identificato da un indirizzo email e il suo account è protetto da una password

> ***Note***
> Gli utenti forniti di default *non* rispettano gli standard di sicurezza di DaraDara in materia di password, ovvero, le loro password sono lunghe meno di 8 caratteri e contengono solo lettere minuscole, tuttavia questo non significa che un nuovo utente non debba rispettare questi standard, infatti ogni nuovo utente, come si potrà notare nella UI, deve rispettare degli standard per quanto riguarda la complessità della password. Questa scelta è stata fatta per facilitare il debugging dell'applicazione.

#### Creatori

* John Doe (email: `john.doe@email.com`  password: `john`)
* Jane Smith (email: `jane.smith@email.com` password: `jane`)
* Robert Johnson (email: `robert.johnson@email.com` password: `robert`)
* Michael Brown (email: `michael.brown@email.com` password: `michael`)

#### Ascoltatori

* Emily Williams (email: `emily.williams@email.com` password: `emily`)
* Massimiliano Carli (email: `admin@daradara.it` password: `admin`)

### Podcast (serie)

In DaraDara ci sono già 6 serie, solo Soccer e Basketball dispongono già di alcuni episodi, le altre non hanno nessun episodio

Alcuni utenti già seguono alcune serie, altri ancora hanno già salvato degli episodi. Queste informazioni sono facilmente reperibili del database data.db dentro la cartella data, nelle tabelle saves e follows

* Soccer (di John)
* Baseball (di John)
* Golf (di John)
* Football (di Robert)
* Basketball (di Jane)
* Tennis (di Michael)

## Risorse utilizzate

DaraDara è stato scritto utilizzando i seguenti linguaggi:

* HTML
* CSS
* JavaScript
* Python (server-side)

DaraDara è stato inoltre creato utilizzando varie librerie e risorse esterne, tutte elencate qui sotto:

1. [Flask](https://flask.palletsprojects.com/en/2.2.x/) ([Flask-Login](https://pypi.org/project/Flask-Login/) e [Flask-Session](https://pypi.org/project/Flask-Session/)) abbinato con [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) per servire la pagine web
2. [Bootstrap](https://getbootstrap.com/) per standardizzare e rendere più intuitiva e responsive la UI
3. [SQLite](https://www.sqlite.org/index.html) per salvare i dati in maniera permanente
4. [Googlefonts](https://fonts.google.com/specimen/League%20Spartan) e [Fontawesome](https://fontawesome.com/icons) per font e icone utilizzate nell'applicazione
5. La collezione di immagini [TechLife](https://blush.design/it/collections/EcYTq93px20ptlPRSq1C/tech-life) di Karthik Srinivas per rendere la UI/UX più piacevole
6. Il sito di design [Canva](https://www.canva.com/it_it/) per sviluppare il logo visibile nella barra di navigazione
7. I siti [Pexels](https://www.pexels.com/it-it/) e [FreeMusicArchive](https://freemusicarchive.org/home) per reperire le immagini e gli audio già presenti nell'applicazione
8. Le librerie python [Dateutil](https://pypi.org/project/python-dateutil/) e [Pillow](https://pypi.org/project/Pillow/)
9. La libreria javascript [Dayjs](https://day.js.org/) per gestire al meglio le date client-side
