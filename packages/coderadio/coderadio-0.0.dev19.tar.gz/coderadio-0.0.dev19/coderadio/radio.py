import mpv

from streamscrobbler import streamscrobbler
from pyradios import RadioBrowser


import re
import importlib
import logging


log = logging.getLogger(__name__)


class Metadata:
    def __init__(self):
        self.station = None

    def fetch(self):
        """
        Try to get metadata from the plugin or streamscrobbler.
        """
        song, service = self.get_metadata_from_plugin(
            self.station
        )
        if song and service:
            return song, service
        else:
            song = self.get_metadata_from_stream(
                self.station.url
            )
            return song, self.station.homepage

    def _plugin_name(self, station):
        name = self._normalize_plugin_name(station.name)
        return "plug_{}".format(name.lower())

    def get_metadata_from_plugin(self, station):
        try:
            plugin = importlib.import_module(
                "coderadio.plugins." + self._plugin_name(station)
            )
        except ImportError:
            log.exception("Plugin not Found")
            return None, None
        else:
            service, artist, title = plugin.run()
            if not all([service, artist, title]):
                return
            song = "{} - {}".format(artist, title)
        return song, service

    def _normalize_plugin_name(self, name):
        return re.sub(r"(\s|\-|\.|,|\"|\'|\`)+", "_", name)

    def get_metadata_from_stream(self, url):
        data = streamscrobbler.get_server_info(url)
        metadata = data["metadata"]
        if not metadata:
            return
        return metadata.get("song")

    def __call__(self, station):
        self.station = station


def click_counter(stationuuid):
    try:
        station = rb.click_counter(stationuuid)
    except Exception:
        log.exception("Playable Station Error:")
    else:
        return station["url"]


def search(**kwargs):
    command = kwargs.get("command")
    term = kwargs.get("term")
    result = getattr(rb, "stations_by_{}".format(command[2:]))(term)
    return result


class MpvPlayer:
    def __init__(self, **kwargs):
        self.player = mpv.MPV(
            video=False,
            ytdl=False,
            input_default_bindings=True,
            input_vo_keyboard=True,
        )
        self.player.fullscreen = False
        self.player.loop_playlist = "inf"
        self.player["vo"] = "gpu"
        self.player.set_loglevel = "no"

    def play(self, url):
        self.player.play(url)
        # self.player.wait_for_playback() # Block

    def stop(self):
        self.player.play("")

    def pause(self):
        if self.player.pause:
            self.player.pause = False
        else:
            self.player.pause = True

    def terminate(self):
        self.player.terminate()


class Player:
    def __init__(self, **kwargs):
        self.player = MpvPlayer()

    def play(self, stationuuid):
        url = click_counter(stationuuid)
        self.player.play(url)

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def terminate(self):
        self.player.terminate()


rb = RadioBrowser()
player = Player()
metadata = Metadata()
