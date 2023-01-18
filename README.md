# DaraDara

DaraDara è una semplice applicazione web per l'ascolto e la condivisione di podcast.

Il nome deriva dall'onomatopea giapponese「だらだら」che, secondo [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), si usa per indicare che una persona sta "parlando o spiegando qualcosa di molto poco chiaro e ci sta mettendo tantissimo tempo per farlo"

## Installare le dipendenze

```prompt
pip install -r requirements.txt
```

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
