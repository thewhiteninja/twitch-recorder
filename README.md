# Twitchrec

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nlohmann/json/master/LICENSE.MIT)
[![Language: C++](https://img.shields.io/badge/Language-Python-brightgreen.svg?tyle=flat-square)](#)

<br />

Twitchrec is a Twitch recorder base on the awesome streamlink.

Check an example of stream in the [data](data) folder.

#### Requirements

- [streamlink](https://github.com/streamlink/streamlink)

#### Usage

- Add/Set your .stream file like the example below

      {
        "id": "lestream",
        "timezone": "Europe/Paris",
        "options": {
        },
        "streams": [
          {
            "name": "Le Recap",
            "quality": "720p",
            "days": "Mon,Tue,Wed,Thu,Fri",
            "start": "18:30",
            "end": "20:30"
          }
        ]
      }

- Run main.py


