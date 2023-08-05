from coderadio.messages import emitter
from coderadio.radio import search
from coderadio.radio import player
from coderadio.radio import metadata

from notify import Notification

from asyncio import get_event_loop
from asyncio import CancelledError

background_tasks = []


def create_background_task(coroutine):
    task = get_event_loop().create_task(coroutine)
    background_tasks.append(task)
    return task


def cancel_background_tasks():
    for task in background_tasks:
        task.cancel()


def finalize_services():
    player.terminate()


def initialize_services():
    emitter.on("RADIO_PLAY", player.play)
    emitter.on("RADIO_STOP", player.stop)
    emitter.on("RADIO_PAUSE", player.pause)
    emitter.on("RADIO_SEARCH", search)
    emitter.on("METADATA_INIT", metadata)
    emitter.on("METADATA_FETCH", metadata.fetch)
    emitter.on("NOTIFICATION", Notification)
    emitter.on("KILLALL", finalize_services)
