# DaraDara

DaraDara è un'applicazione web per l'ascolto e la pubblicazione di podcast.

Il nome deriva dall'onomatopea giapponese「だらだら」che, secondo [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), si usa per indicare il "vocio" che si crea quando una persona sta "parlando o spiegando qualcosa di molto poco chiaro e ci sta mettendo tantissimo tempo per farlo"

## Installazione veloce

Per avviare l'applicazioe è sufficente collocarsi nel percorso file opportuno e digitare i seguenti comandi sul proprio terminale

```prompt
pip install -r requirements.txt
flask run
```

Dopodichè sarà necessario aprirle una pagina web all'inidirizzo ```127.0.0.1:5000``` nel proprio browser preferito (Google Chrome o Firefox).

## Dispositivi compatibili

DaraDara è ideato per funzionare sui moderni smartphone, tablet e desktop (tutti i dispositivi con almeno 350px di larghezza e 600x di altezza)

DaraDara è responsive e si adatta alle dimensoni di vari schermi grazie all'utilizzo di bootstrap

## Alcune linee guida per utilizzare DaraDara

Qui sotto potete trovare elencate una serie di linee guida utili per utilizzare e debuggare DaraDara

### Come posso registrarmi?

Non esiste un tasto che dalla homepage rimandi direttamente alla registrazione, bisogna prima dirigersi nella pagina di login con il tasto accedi e poi premere sulla scritta rossa "Registrati!"

### Cosa indicano le icone dell'occhio nel profilo?

Ogni icona rappresentante un occhio che indica se si vuole tenere quella data sezione del profilo pubblica o privata a gli altri utenti. Se l'icona è un normale un occhio allora la data sezione è pubblica a gli altri utenti, se c'è una barra sopra l'occhio allora la sezione è privata e solo il proprietario del profilo può vederla

### Come scegli i podcast più in voga?

I 4 podcast più in voga, visualizzabili esclusivamente nella home, sono i podcast con più seguaci su DaraDara, condizione necesaria affinché un podcast possa finire in voga è di aver almeno 1 seguace e almeno 1 episodio

> Se ci sono meno di 4 podcast con almeno 1 seguace e 1 episodio vengono visualizzati quanti ve ne sono

### Cosa fa il tasto "sorprendimi"?

Il tasto "sorprendimi", presente nella navabar, sceglie semplicemente a caso un podcast tra i vari disponibili su DaraDara e lo mostra all'utente

### Reset dei dati di Flask

Per facilitare il debug sono state aggiunte due root "nascoste" per ripulire i dati relativi a Flask-Session e Flask-Login, da utilizzare al bisogno.

* Route per ripulire le sessioni: ```/clear_session```
* Route per ripulire il login: ```/clear_login```

Si consieri che queste route non sarebbero ovviamente pubblicate in un applicazione web aperta al pubblico, sono da utilizzare solo a scopo di debugging.

## Utenti e serie già presenti

DaraDara è già fornito di alcuni dati di esempio per fornire un esperienza utente basilare per testare tutte le feature messe a disposizione e richieste dal tema d'esame

### Utenti

In DaraDara ci sono già 6 utenti: **2 ascoltatori** e **4 creatori**

Ogni utente è identificato da un indirizzo email e il suo account è protetto da una password

> ***Note***
> Per motivi di debugging gli utenti forniti di default *non* rispettano gli standard di sicurezza di DaraDara in materia di password, ovvero le loro password sono lunghe meno di 8 caratteri e contengono solo lettere minuscole. Tuttavia questo non significa che un nuovo utente non debba rispettare questi standard, infatti ogni nuovo utente, come si potrà notare nella UI, deve rispettare una serie di regole in fase di registrazione per quanto riguarda la complessità della password

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
5. La collezione di immagini [TechLife](https://blush.design/it/collections/EcYTq93px20ptlPRSq1C/tech-life) di Karthik Srinivas per rendere la UI più gradevole
6. Il sito di design [Canva](https://www.canva.com/it_it/) per sviluppare il logo visibile nella barra di navigazione e come .ico nella scheda del browser
7. I siti [Pexels](https://www.pexels.com/it-it/) e [FreeMusicArchive](https://freemusicarchive.org/home) per reperire le immagini e gli audio già presenti nell'applicazione
8. Le librerie python [Dateutil](https://pypi.org/project/python-dateutil/) e [Pillow](https://pypi.org/project/Pillow/) per gestire le date e la modifica delle immagini server-side
9. La libreria javascript [Dayjs](https://day.js.org/) per gestire le date client-side
