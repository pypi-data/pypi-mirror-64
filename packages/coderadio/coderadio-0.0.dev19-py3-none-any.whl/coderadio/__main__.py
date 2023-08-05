from coderadio.tui import app
from coderadio import initialize_services


def main():
    initialize_services()
    app.run()
