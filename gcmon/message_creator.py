from pychromecast import Chromecast
from pychromecast.controllers.media import MediaStatus

from gcmon.types import MessageCreatorInterface


def format_movie(status):
    return {
        "type": "movie",
        "title": status.title,
    }


def format_music(status):
    return {
        "type": "music",
        "title": status.title,
        "artist": status.artist,
        "album": status.album_name,
        "track": status.track,
    }


def format_tv(status):
    return {
        "type": "tv",
        "title": status.title,
    }


def format_photo(status):
    return {
        "type": "photo",
        "title": status.title,
    }


def format_generic(status):
    return {
        "type": "generic",
        "title": status.title,
    }


class MessageCreator(MessageCreatorInterface):
    def create_message(self, device: Chromecast, status: MediaStatus):
        return {
            "contentId": status.content_id,
            "sessionId": status.media_session_id,
            "device": device.name,
            "state": status.player_state,
            "volume": status.volume_level if not status.volume_muted else 0,
            "currentTime": status.current_time,
            "duration": status.duration,
            "images": [m.url for m in status.images],
            "media": self.format_media(status)
        }

    def format_media(self, status: MediaStatus):
        if status.media_is_movie:
            return format_movie(status)
        elif status.media_is_musictrack:
            return format_music(status)
        elif status.media_is_tvshow:
            return format_tv(status)
        elif status.media_is_photo:
            return format_photo(status)
        elif status.media_is_generic:
            return format_generic(status)
        else:
            return {"title": status.title, "type": "unknown"}
