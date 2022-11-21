import glob
import os
import sys

import utils
from recorder import StreamRec

OUTDIR = ""


def parse_args(a):
    global OUTDIR
    i = 1
    while i < len(a):
        if a[i] in ["-h", "--help", "/?"]:
            usage()
        if a[i] in ["-d", "--dir"]:
            OUTDIR = a[i + 1]
            i += 1
        i += 1


def usage():
    print("Record your favorite Twitch streams!")
    print("Check an example of .stream file in data/ to see how to add a stream to record")
    print()
    print("Usage: %s [Options]" % (os.path.basename(sys.argv[0])))
    print()
    print("Options :")
    print("    -d, --dir : Output directory")
    print("    -h, --help : Help")
    sys.exit(1)


def load_streams():
    all_inst = []
    stream_files = glob.glob('data/**/*.stream', recursive=True)
    for stream_file in stream_files:
        inst = StreamRec(stream_file, OUTDIR)
        all_inst.append(inst)
    for inst in all_inst:
        inst.start()
    for inst in all_inst:
        inst.join()


def main():
    utils.welcome()
    parse_args(sys.argv)
    if utils.check_streamlink_version():
        utils.make_directory(OUTDIR)
        load_streams()
    else:
        utils.log("Streamlink version >= 5.1.0 required!")
        utils.log("Download it here: https://github.com/streamlink/windows-builds/releases/")


if __name__ == '__main__':
    main()
