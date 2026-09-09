#!/usr/bin/python3
#
# SoundConverter - GNOME application for converting between audio formats.
# Copyright 2004 Lars Wirzenius
# Copyright 2005-2025 Gautier Portet
# Copyright 2020-2025 Sezanzeb
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA


from soundconverter.util.logger import logger
from soundconverter.util.settings import get_gio_settings

filename_denylist = ("*.iso",)


def get_mime_type_mapping():
    """Return a mapping of file extension to mime type."""
    return {
        "ogg": "audio/x-vorbis",
        "flac": "audio/x-flac",
        "wav": "audio/x-wav",
        "mp3": "audio/mpeg",
        "aac": "audio/x-m4a",
        "m4a": "audio/x-m4a",
        "opus": "audio/ogg; codecs=opus",
        "wma": "audio/x-ms-wma",
    }


def get_mime_type(audio_format):
    """Return the matching mime-type or None if it is not supported.

    Parameters
    ----------
    audio_format : string
        for example 'mp3' or 'audio/mpeg' for which the result would
        be 'audio/mpeg'
    """
    mime_types = get_mime_type_mapping()
    if audio_format not in mime_types.values():
        # possibly a file extension
        return mime_types.get(audio_format, None)
    # already a mime string
    return audio_format


def get_file_extension(mime):
    """Return the matching file extension or '?' if it is not supported.

    Examples: 'mp3', 'flac'.

    Parameters
    ----------
    mime : string
        mime string (like 'audio/x-m4a')
    """
    mime_types = get_mime_type_mapping()
    if mime in mime_types:
        # already an extension
        suffix = mime
    else:
        mime2ext = {mime: ext for ext, mime in mime_types.items()}
        suffix = mime2ext.get(mime, "?")
    if suffix == "ogg":
        if get_gio_settings().get_boolean("vorbis-oga-extension"):
            suffix = "oga"
    return suffix


def get_quality_setting_name():
    """Get the settings name for quality for the set output-mime-type."""
    settings = get_gio_settings()
    mime_type = settings.get_string("output-mime-type")
    if mime_type == "audio/mpeg":
        mode = settings.get_string("mp3-mode")
        setting_name = {
            "cbr": "mp3-cbr-quality",
            "abr": "mp3-abr-quality",
            "vbr": "mp3-vbr-quality",
        }[mode]
    else:
        setting_name = {
            "audio/x-vorbis": "vorbis-quality",
            "audio/x-m4a": "aac-vbr-preset",
            "audio/ogg; codecs=opus": "opus-bitrate",
            "audio/x-flac": "flac-compression",
            "audio/x-ms-wma": "wma-bitrate",
            "audio/x-wav": "wav-sample-width",
        }[mime_type]
    return setting_name


def get_bitrate_from_settings():
    """Get a human readable bitrate from quality settings.

    For example '~224 kbps'
    """
    settings = get_gio_settings()
    mime_type = settings.get_string("output-mime-type")
    mode = settings.get_string("mp3-mode")

    bitrate = 0
    approx = True

    if mime_type == "audio/x-vorbis":
        quality = settings.get_double("vorbis-quality")
        quality = max(-0.1, min(1.0, quality))
        quality_index = round((quality + 0.1) * 10)
        bitrates = (
            45,   # Q-1
            64,   # Q0
            80,   # Q1
            96,   # Q2
            112,  # Q3
            128,  # Q4
            160,  # Q5
            192,  # Q6
            224,  # Q7
            256,  # Q8
            320,  # Q9
            500,  # Q10
        )
        bitrate = bitrates[quality_index]

    elif mime_type == "audio/x-m4a":
        return "N/A"

    elif mime_type == "audio/ogg; codecs=opus":
        bitrate = settings.get_int("opus-bitrate")

    elif mime_type == "audio/x-ms-wma":
        bitrate = settings.get_int("wma-bitrate")

    elif mime_type == "audio/mpeg":
        mp3_quality_setting_name = {
            "cbr": "mp3-cbr-quality",
            "abr": "mp3-abr-quality",
            "vbr": "mp3-vbr-quality",
        }[mode]
        setting = settings.get_int(mp3_quality_setting_name)
        if mode == "vbr":
            # depends on the input audio
            return "N/A"
        if mode == "cbr":
            approx = False
            bitrate = setting
        if mode == "abr":
            bitrate = setting

    elif mime_type == "audio/x-wav":
        approx = False
        output_resample = settings.get_boolean("output-resample")
        resample_rate = settings.get_int("resample-rate")
        sample_width = settings.get_int("wav-sample-width")
        if output_resample:
            bitrate = sample_width * resample_rate / 1000
        else:
            # the actual bitrate will depend on the input audio, which
            # cannot be known in the settings menu beforehand. Assume 44100
            # which is the most common.
            bitrate = sample_width * 44100 / 1000

    if bitrate:
        if approx:
            return f"~{bitrate} kbps"
        return f"{bitrate} kbps"
    return "N/A"


def get_default_quality(mime, mode="vbr"):
    """Return a default quality if the -q parameter is not set.

    Parameters
    ----------
    mime : string
        mime type
    mode : string
        one of 'cbr', 'abr' and 'vbr' for mp3
    """
    # Default quality values for each output format
    default = {
        "audio/x-vorbis": 0.6,
        "audio/x-m4a": 3,
        "audio/ogg; codecs=opus": 192,
        "audio/mpeg": {
            "cbr": 320,
            "abr": 192,
            "vbr": 2,  # inverted !
        },
        "audio/x-wav": 16,
        "audio/x-flac": 5,
        "audio/x-ms-wma": 192,
    }[mime]

    if isinstance(default, dict):
        default = default[mode]

    return default


def get_quality(mime, value, mode="vbr", reverse=False):
    """Map a quality index to the corresponding format-specific value.

    Parameters
    ----------
    mime : string
        MIME type of the output format.
    value : number
        Quality index, or a format-specific quality value when reverse=True.
        An index of -1 selects the highest available quality.
    mode : string
        One of 'cbr', 'abr', and 'vbr' for MP3.
    reverse : bool
        If False, return the format-specific quality value for the given
        index. If True, return the index corresponding to the given
        format-specific quality value.
    """

    # get all available qualities
    qualities = {
        "audio/x-vorbis": (-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
        "audio/ogg; codecs=opus": (6, 9, 10, 12, 16, 24, 32, 40, 48, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 512, 650),
        "audio/mpeg": {
            "cbr": (8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
            "abr": (8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
            "vbr": (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),  # inverted !
        },
        "audio/x-wav": (8, 16, 24, 32),
        "audio/x-flac": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        "audio/x-ms-wma": (64, 96, 128, 160, 192, 224, 256, 320),
    }[mime]

    if isinstance(qualities, dict):
        qualities = qualities[mode]

    # return depending on function parameters
    if reverse:
        if isinstance(value, float):
            # floats are inaccurate, search for close value
            for i, quality in enumerate(qualities):
                if abs(value - quality) < 0.01:
                    return i

        if value in qualities:
            return qualities.index(value)

        # might be some custom value set e.g. in batch mode.
        # the reverse mode is only interesting for the ui though, because
        # it has predefined qualities as opposed to batch. So this is
        # either a setting leaking from some tests or the batch mode
        # persisted something.
        if mime == "audio/mpeg":
            ftype_mode = f"{mime} {mode}"
        else:
            ftype_mode = mime
        logger.warning(f"tried to index unknown {ftype_mode} quality {value}")
        return None
    # normal index
    if value < -len(qualities) or value >= len(qualities):
        raise ValueError(
            f"quality index {value} has to be between "
            f"{-len(qualities)} and {len(qualities) - 1}",
        )
    return qualities[value]
