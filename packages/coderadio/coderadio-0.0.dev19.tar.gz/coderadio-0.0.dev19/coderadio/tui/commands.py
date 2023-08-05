from prompt_toolkit.contrib.regular_languages import compile
from prompt_toolkit.document import Document
from prompt_toolkit.application.current import get_app

from coderadio.tui.constants import DISPLAY_BUFFER
from coderadio.tui.constants import PROMPT_BUFFER
from coderadio.tui.constants import LISTVIEW_BUFFER
from coderadio.tui.constants import POPUP_BUFFER
from coderadio.tui.constants import HELP_TEXT

from coderadio import create_background_task
from coderadio import cancel_background_tasks
from coderadio import background_tasks

from coderadio.messages import emitter
from coderadio.utils import CurrentStation
from coderadio.utils import stations

import asyncio
import logging


log = logging.getLogger(__name__)


COMMAND_GRAMMAR = compile(
    r"""(
        (?P<command>[^\s]+) \s+ (?P<subcommand>[^\s]+) \s+ (?P<term>[^\s].+) |
        (?P<command>[^\s]+) \s+ (?P<term>[^\s]+) |
        (?P<command>[^\s!]+)
    )"""
)


COMMAND_TO_HANDLER = {}


current_station = CurrentStation()


async def current_station_notify():
    while True:
        metadata = emitter.emit("METADATA_FETCH")
        log.info(metadata)
        emitter.emit(
            "NOTIFICATION",
            metadata[0],
            title=metadata[1]
        )
        await asyncio.sleep(current_station.period)


def has_command_handler(command):
    return command in COMMAND_TO_HANDLER


def call_command_handler(command, *args, **kwargs):
    COMMAND_TO_HANDLER[command](*args, **kwargs)


def get_commands():
    return COMMAND_TO_HANDLER.keys()


def get_command_help(command):
    return COMMAND_TO_HANDLER[command].__doc__


def listview_handler(event):
    call_command_handler("play", event)


def prompt_handler(event):
    variables = COMMAND_GRAMMAR.match(
        event.current_buffer.text).variables()
    command = variables.get("command")
    if has_command_handler(command):
        call_command_handler(command, event, variables=variables)


def cmd(name):
    """
    Decorator to register commands in this namespace
    """
    def decorator(func):
        COMMAND_TO_HANDLER[name] = func
    return decorator


@cmd("exit")
def exit(event, **kwargs):
    """ exit Ctrl + Q"""
    emitter.emit("KILLALL")
    get_app().exit()


@cmd("play")
def play(event, **kwargs):
    call_command_handler("stop", event)
    list_buffer = event.app.layout.get_buffer_by_name(
        LISTVIEW_BUFFER
    )
    display_buffer = event.app.layout.get_buffer_by_name(
        DISPLAY_BUFFER
    )
    # escolher nome descitivo para o metodo get_index
    index = list_buffer.get_index(**kwargs)
    station = stations[int(index)]
    emitter.emit("RADIO_PLAY", station.stationuuid)
    emitter.emit("METADATA_INIT", station)
    current_station.current = station
    display_buffer.update(current_station.info())
    create_background_task(current_station_notify())


@cmd("stop")
def stop(event, **kwargs):
    display_buffer = event.app.layout.get_buffer_by_name(
        DISPLAY_BUFFER
    )
    display_buffer.clear()
    emitter.emit("RADIO_STOP")
    if background_tasks:
        cancel_background_tasks()


@cmd("pause")
def pause(event, **kwargs):
    emitter.emit("RADIO_PAUSE")


@cmd("list")
def list(event, **kwargs):
    list_buffer = event.app.layout.get_buffer_by_name(
        LISTVIEW_BUFFER
    )
    subcommand = kwargs["variables"].get("subcommand")
    term = kwargs["variables"].get("term")
    resp = emitter.emit(
        "RADIO_SEARCH",
        command=subcommand,
        term=term
    )
    stations.new(*resp)
    list_buffer.update(str(stations))


@cmd("nowplaying")
def nowplaying(event, **kwargs):
    variables = kwargs.get("variables")
    subcommand = variables.get("subcommand", None)
    term = variables.get("term", None)
    if subcommand == 'period':
        current_station.period = term
        if background_tasks:
            cancel_background_tasks()
        create_background_task(current_station_notify())

@cmd("help")
def help(event, **kwargs):
    """ show help """
    popup_buffer = event.app.layout.get_buffer_by_name(
        POPUP_BUFFER
    )
    popup_buffer.update(HELP_TEXT)
    get_app().layout.focus(popup_buffer)
