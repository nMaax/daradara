# DaraDara

DaraDara è una semplice applicazione web per l'ascolto e la condivisione di podcast.
Il nome deriva dall'onomatopea giapponese「だらだら」che, secondo [Tofugu](https://www.tofugu.com/japanese/japanese-onomatopoeia/), si usa per indicare che una persona sta "parlando o spiegando qualcosa di molto poco chiaro e ci sta mettendo tantissimo tempo per farlo"

## Come avviare DaraDara

Per avviare DaraDara sulla propria macchina è necessario:

1. Avere un browser web
2. Avere python installato

Dopodiché è necessario installare le seguenti librerie:

1. Flask
2. Flask-Session
3. Flask-Login
4. pyhton-dateutil

## Risorse utilizzate

DaraDara è stato scritto in HTML, CSS, JavaScript (client-side) e Python (server-side)

DaraDara è stato creato utilizzando varie risorse esterne, tutte elencate qui sotto:

1. Flask (Flask-Login e Flask-Session) abbinato con Jinja per servire la pagine web
2. Bootstrap per standardizzare e rendere più intuitiva la UI
3. SQLite per salvare i dati in maniera permanente
4. Dayjs (libreria esterna js) per gestire al meglio le date client-side
5. Howler (libreria esterna js) per gestire la riproduzione audio in maniera più sofisticata
6. Googlefonts e Fontawesome per font e icone utilizzate nell'applicazione
7. Humaaans, Paaaterns e Avataaars per il design generale dell'applicazione
8. Varie librerie python utili all'elaborazione dei dati nel lato server (solo dateutil non è nativamente installata)
