# NewsWave

**NewsWave** is an advanced **RSS** feed reader designed to curate daily news and deliver it conveniently to your email. Please note that it is currently a work in progress, and contributions are welcome.

## Getting Started

To initiate the search for news and have it sent to your email, execute the following command in your terminal:

```bash
python main.py
```

## Configuring SMTP Server and Email Settings

Customize your SMTP server and email parameters by editing the *config.ini* file. Adjust the SMTP type, server, port, user, and password settings:

```ini
[SMTP]
TYPE = SSL
SERVER = smtp.gmail.com
PORT = 465
USER = your_email@gmail.com
PASSWORD = as9xs3nckscjsxuw
[EMAIL]
FROM = from_email@gmail.com
TO = to_email@gmail.com
SUBJECT = NewsWave
BODY = Todays news from your RSS feeds
ATTACHMENT = NewsWave.html
```

Valid SMTP types are NORMAL, SSL, and TSL. If you are using the GMail SMTP server, note that the *PASSWORD* field must be a valid token, not your current password.

## Managing Feeds

Access the web interface to manage your feeds, including listing, adding, editing, or deleting them. Start the server and visit [localhost:5000](http://localhost:5000/):

```bash
python server.py
```

## Scheduling Execution

Automate the execution using Task Scheduler in Windows or Cron in Linux.

## Installing and Dependencies

NewsWave requiere Python3.10+ to works. Also, *Feedparser* and *Flask* are required too.

### Installing with VirtualEnv

```bash
git clone https://github.com/xurxia/newswave.git
python -m venv newswave
cd newswave
source bin/activate
pip install -r requirements.txt
```

### Installing without VirtualEnv

```bash
git clone https://github.com/xurxia/newswave.git
cd newswave
pip install -r requirements.txt
```
## To-Do List

- [ ] Add categories to sort and join feeds
- [ ] Implement Jinja2 as the template engine for rendering the output
- [ ] Add support for additional databases (MySQL and Postgres)
- [X] Implement link filtering before sending
- [X] Develop a usage tutorial (Work in Progress)
- [X] Capture and manage exceptions and errors
- [X] Integrate a web interface for feed management
- [X] Utilize the Factory pattern to instantiate SMTP connections
- [X] Incorporate SSL and TSL support for SMTP
- [X] Implement the Factory pattern for instantiating database connections

## Contact
For further information or inquiries, feel free to reach out via Mastodon, Matrix or Email:

🐘 [Mastodon](https://astrodon.social/@xurxia)<br>
💬 [Matrix](https://matrix.to/#/@xurxia:matrix.tchncs.de)<br>
✉️ [Email](info@xurxia.net)<br>
