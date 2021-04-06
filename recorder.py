import calendar
import datetime
import json
import os
import subprocess
import time
from threading import Thread

import pytz

from utils import log


def make_datetime(t, tz):
    time = datetime.datetime.strptime(t, '%H:%M')
    date = datetime.datetime.now().replace(hour=time.hour, minute=time.minute, second=0)
    date = pytz.timezone(tz).localize(date, is_dst=None)
    return date


def make_days(stream):
    days = []
    cst_days = list(map(str, calendar.day_abbr))
    for d in stream["days"].split(","):
        if d in cst_days:
            days.append(cst_days.index(d))
    return days


class StreamRec(Thread):
    def __init__(self, config, outdir):
        Thread.__init__(self)
        log("Loading %s" % config)
        f = open(config, "r")
        self.config = json.load(f)
        f.close()
        self.outdir = outdir

    def get_next_stream(self):
        next_stream, next_wait, next_duration = 0, 0, 0
        for i in range(len(self.config["streams"])):
            stream = self.config["streams"][i]
            begin = make_datetime(stream["start"], self.config["timezone"])
            end = make_datetime(stream["end"], self.config["timezone"])
            days = make_days(stream)
            now = datetime.datetime.now(pytz.timezone(self.config["timezone"]))

            while begin < now or begin.weekday() not in days:
                if now < end and begin.weekday() in days:
                    begin = now
                else:
                    begin += datetime.timedelta(days=1)
                    end += datetime.timedelta(days=1)

            s_wait = (begin - now).total_seconds()
            if s_wait < next_wait or i == 0:
                next_stream, next_wait, next_duration = i, s_wait, (end - begin).total_seconds()

        return next_stream, next_wait, next_duration

    def build_args(self, stream):
        begin = make_datetime(stream["start"], self.config["timezone"])

        args = ["streamlink"]
        for o in self.config["options"].keys():
            args.append("--" + o)
            args.append(self.config["options"][o])
        args.append("twitch.tv/" + self.config["id"])
        args.append(stream["quality"])
        filename = "%s_%s_%02d_%02d%02d.mp4" % (
            stream["name"].replace(" ", "_"), list(calendar.day_abbr)[begin.weekday()], begin.day, begin.hour,
            begin.minute)
        output_file = os.path.join(self.outdir, filename)
        args.append("-o")
        args.append("'%s'" % (output_file))

        return args, output_file

    def run(self):
        while True:
            next_stream, next_wait, next_duration = self.get_next_stream()
            stream = self.config["streams"][next_stream]
            log("Next stream \"%s\" (%s) at %s" % (stream["name"], stream["quality"], stream["start"]))
            time.sleep(next_wait)
            args, output_file = self.build_args(stream)
            log("Command: " + (" ".join(args)))
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log("Recording %s ..." % stream["name"])
            time.sleep(8)
            no_stream = proc.poll()
            if no_stream is not None:
                log("No playable streams for now")
                log("Waiting for the next stream...")
            time.sleep(next_duration)
            if no_stream is None:
                proc.terminate()
                log("End of stream")
