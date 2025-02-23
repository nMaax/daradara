# DaraDara (in Italian) - ***English version below!***

DaraDara è un'applicazione web per l'ascolto e la pubblicazione di podcast.

Il nome deriva dall'onomatopea giapponese「だらだら」che, secondo [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), si usa per indicare il "rumore" che si crea quando una persona sta "parlando o spiegando qualcosa di molto poco chiaro e ci sta mettendo tantissimo tempo per farlo"

## Installazione veloce 🚀

Per avviare l'applicazione è sufficente collocarsi nel percorso file opportuno e digitare i seguenti comandi sul proprio terminale

```prompt
pip install -r requirements.txt
flask run
```

Dopodichè sarà necessario aprire una pagina web all'inidirizzo ```127.0.0.1:5000``` nel proprio browser preferito (Google Chrome o Firefox).

Per terminare l'applicazione basterà premere ```CTRL + C``` ripetutamente nello stesso terminale

### Installazione con virtual enviroment

Eventualmente, se non si volessero installare le dipendenze pyhton contenute in requirements.txt a livello globale, prima di avviare i comandi sopra elencati, è possibile creare e attivare un *python virtual enviroment* con i seguenti comandi

Per macchine *OSX / Linux*

```prompt
python3 -m venv venv
. venv/bin/activate
```

Per macchine *Windows*

```prompt
python -m venv venv
. venv/Scripts/activate
```

per terminare il virtual enviroment è sufficiente digitate ```deactivate``` sempre nello stesso terminale

## Dispositivi compatibili 📲

DaraDara è ideato per funzionare sui moderni smartphone, tablet e desktop (tutti i dispositivi con almeno 375px di larghezza e 600x di altezza)

DaraDara è responsive e si adatta alle dimensoni di vari schermi grazie all'utilizzo di bootstrap

## Alcune linee guida per utilizzare DaraDara

Qui sotto potete trovare elencate una serie di linee guida per utilizzare e debuggare DaraDara

### Come posso registrarmi a DaraDara?

Non esiste un tasto che dalla homepage rimandi direttamente alla registrazione, bisogna prima dirigersi nella pagina di login con il tasto accedi e poi premere sulla scritta rossa "Registrati!"

### Cosa indicano le icone dell'occhio nel profilo?

Ogni icona rappresentante un occhio che indica se si vuole tenere quella data sezione del profilo pubblica o privata a gli altri utenti. Se l'icona è un normale un occhio allora la data sezione è pubblica a gli altri utenti, se c'è una barra sopra l'occhio allora la sezione è privata e solo il proprietario del profilo può vederla

### Come scegli i podcast più in voga?

I 4 podcast più in voga, visualizzabili esclusivamente nella home, sono i podcast con più seguaci su DaraDara, condizione necesaria affinché un podcast possa finire in voga è di aver almeno 1 seguace e almeno 1 episodio

> ***Note***
> Se ci sono meno di 4 podcast con almeno 1 seguace e 1 episodio vengono visualizzati quanti se ne può

### Cosa fa il tasto "sorprendimi" nella navabar?

Il tasto "sorprendimi", presente nella navabar, sceglie semplicemente a caso un podcast tra i vari disponibili su DaraDara e lo mostra all'utente

### Reset dei dati di Flask

Per facilitare il debug sono state aggiunte due root "nascoste" per ripulire i dati relativi a Flask-Session e Flask-Login, da utilizzare al bisogno.

* Route per ripulire le sessioni: ```/clear_session```
* Route per ripulire il login: ```/clear_login```

Si consieri che queste route non sarebbero ovviamente pubblicate in un applicazione web aperta al pubblico, sono da utilizzare solo a scopo di debugging.

### Reset del database

In aggiunta è possibile trovare dentro la cartella ```data``` una sottocartella chiamata ```backup``` dove vi risiedono alcuni file utili a riprendere un backup passato del database

Vi si possono già trovare

* 1 copia di backup del database chiamata ```data.db``` con tutti i dati di default forniti con questo progetto senza le eventuali aggiunte che possono essere state fatte durante il debugging dell'app
* 1 database vuoto chiamato ```empty.db``` con la stessa struttura di questo database, dov'é possibile riempirlo di dati nuovi, eventualmente con lo script ```dao_filler.py```
* 1 script python chiamato ```dao_filler.py``` che attraverso il DAO aggiunge i dati di base forniti con questo progetto

Si consideri che l'app è progettata per avere un minimo di serie ed episodi e **non** per essere completamente vuota.

## Utenti e serie già presenti 🙋

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

## Risorse utilizzate 🗃️

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

---

# DaraDara (in English)

DaraDara is a web application for listening to and publishing podcasts.

The name comes from the Japanese onomatopoeia「だらだら」which, according to [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), is used to describe the "sound" that happens when a person is "speaking or explaining something very unclear and taking an incredibly long time to do it."

## Quick Installation 🚀

To launch the application, simply navigate to the appropriate file path and run the following commands in your terminal:

```prompt
pip install -r requirements.txt
flask run
```

Then, open a webpage at the address ```127.0.0.1:5000``` in your preferred browser (Google Chrome or Firefox).

To stop the application, just press ```CTRL + C``` repeatedly in the same terminal.

### Installation with Virtual Environment

If you don’t want to install the dependencies listed in `requirements.txt` globally, you can create and activate a *Python virtual environment* before running the above commands, using the following commands:

For *OSX / Linux* machines:

```prompt
python3 -m venv venv
. venv/bin/activate
```

For *Windows* machines:

```prompt
python -m venv venv
. venv/Scripts/activate
```

To deactivate the virtual environment, simply type ```deactivate``` in the same terminal.

## Compatible Devices 📲

DaraDara is designed to work on modern smartphones, tablets, and desktops (any devices with at least 375px width and 600px height).

DaraDara is responsive and adapts to various screen sizes using Bootstrap.

## Guidelines for Using DaraDara

Below you can find a list of guidelines for using and debugging DaraDara.

### How can I register for DaraDara?

There is no button that directly leads to the registration page from the homepage. First, go to the login page using the "Login" button, then click on the red "Register!" text.

### What do the eye icons in the profile mean?

Each eye icon indicates whether a specific section of the profile should be public or private to other users. If the icon is a normal eye, the section is public, and other users can see it. If there is a line above the eye, the section is private, and only the profile owner can view it.

### How do you choose the most popular podcasts?

The 4 most popular podcasts, visible only on the homepage, are the podcasts with the most followers on DaraDara. For a podcast to be considered popular, it must have at least 1 follower and at least 1 episode.

> ***Note***
> If there are fewer than 4 podcasts with at least 1 follower and 1 episode, as many as possible will be displayed.

### What does the "Surprise me" button in the navbar do?

The "Surprise me" button in the navbar randomly selects a podcast from the available ones on DaraDara and shows it to the user.

### Flask Data Reset

For debugging purposes, two "hidden" routes have been added to clear Flask-Session and Flask-Login data, to be used when needed:

* Route to clear sessions: ```/clear_session```
* Route to clear login: ```/clear_login```

These routes would obviously not be published in a public-facing web application and are intended solely for debugging.

### Database Reset

In addition, inside the ```data``` folder, you will find a subfolder called ```backup``` where some files are stored to restore a previous database backup.

Inside, you can find:

* 1 backup copy of the database named ```data.db``` with the default data provided with this project, excluding any changes made during debugging.
* 1 empty database named ```empty.db``` with the same structure as the original database, where you can fill it with new data using the ```dao_filler.py``` script.
* 1 Python script called ```dao_filler.py``` that uses the DAO to add the basic data provided with this project.

Note that the app is designed to have a minimum number of series and episodes, **not** to be completely empty.

## Pre-existing Users and Series 🙋

DaraDara comes with some sample data to provide a basic user experience for testing all the features required by the exam topic.

### Users

DaraDara already has 6 users: **2 listeners** and **4 creators**.

Each user is identified by an email address, and their account is protected by a password.

> ***Note***
> For debugging purposes, the default users *do not* meet the security standards of DaraDara regarding passwords. Specifically, their passwords are shorter than 8 characters and contain only lowercase letters. However, this does not mean a new user can disregard these standards. In fact, every new user, as you will see in the UI, must comply with certain password complexity rules during registration.

#### Creators

* John Doe (email: `john.doe@email.com`, password: `john`)
* Jane Smith (email: `jane.smith@email.com`, password: `jane`)
* Robert Johnson (email: `robert.johnson@email.com`, password: `robert`)
* Michael Brown (email: `michael.brown@email.com`, password: `michael`)

#### Listeners

* Emily Williams (email: `emily.williams@email.com`, password: `emily`)
* Massimiliano Carli (email: `admin@daradara.it`, password: `admin`)

### Podcasts (Series)

DaraDara already contains 6 series, with only Soccer and Basketball having some episodes. The others do not have any episodes.

Some users already follow some series, while others have saved certain episodes. This information can easily be found in the `data.db` database inside the `data` folder, in the `saves` and `follows` tables.

* Soccer (by John)
* Baseball (by John)
* Golf (by John)
* Football (by Robert)
* Basketball (by Jane)
* Tennis (by Michael)

## Resources Used 🗃️

DaraDara was written using the following languages:

* HTML
* CSS
* JavaScript
* Python (server-side)

DaraDara was also created using various libraries and external resources, all listed below:

1. [Flask](https://flask.palletsprojects.com/en/2.2.x/) ([Flask-Login](https://pypi.org/project/Flask-Login/) and [Flask-Session](https://pypi.org/project/Flask-Session/)) paired with [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) to serve the web pages
2. [Bootstrap](https://getbootstrap.com/) to standardize and make the UI more intuitive and responsive
3. [SQLite](https://www.sqlite.org/index.html) to store data permanently
4. [Googlefonts](https://fonts.google.com/specimen/League%20Spartan) and [Fontawesome](https://fontawesome.com/icons) for fonts and icons used in the application
5. The image collection [TechLife](https://blush.design/it/collections/EcYTq93px20ptlPRSq1C/tech-life) by Karthik Srinivas to enhance the UI's appearance
6. The design site [Canva](https://www.canva.com/it_it/) to create the logo seen in the navigation bar and as an .ico in the browser tab
7. The websites [Pexels](https://www.pexels.com/it-it/) and [FreeMusicArchive](https://freemusicarchive.org/home) to obtain the images and audio already included in the app
8. The Python libraries [Dateutil](https://pypi.org/project/python-dateutil/) and [Pillow](https://pypi.org/project/Pillow/) for handling dates and modifying images server-side
9. The JavaScript library [Dayjs](https://day.js.org/) to manage dates client-side
