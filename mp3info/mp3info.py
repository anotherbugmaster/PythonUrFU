"""Mp3 info main module"""
#!usr/bin/python3

import platform
import argparse
import os
import id3v1
import id3v2
import frame

def main():
    """Main module"""
    parser = argparse.ArgumentParser("Shows MP3 and ID3 info.")
    parser.add_argument("filename", help="Filename")
    parser.add_argument(
        "-p", "--play", action="store_true",
        help="Plays file with default OS player")
    args = parser.parse_args()

    id3v1_items = sorted(id3v1.get_info(args.filename).items())
    id3v2_items = sorted(id3v2.get_info(args.filename).items())
    frame_items = sorted(frame.get_info(args.filename).items())

    try:
        if id3v1_items:
            print("\nID3v1:\n")
            for key, value in id3v1_items:
                print("%-40s %s" % (key + ":", value))
        else:
            print('No ID3v1')
        if id3v2_items:
            print("\nID3v2:\n")
            for key, value in id3v2_items:
                print("%-40s %s" % (key + ":", value))
        else:
            print('No ID3v2')
        if frame_items:
            print("\nFRAME:\n")
            for key, value in frame_items:
                print("%-40s %s" % (key + ":", value))
        else:
            print('No frame info')

        print("\nAdditional:\n")
        filesize = os.path.getsize(args.filename) / pow(2, 20)
        filesize = round(filesize, 2)
        print("Size: %s Mb" % filesize)

        if args.play:
            try:
                if platform.system() == "Windows":
                    os.system("\"" + args.filename+"\"")
                else:
                    os.system("xdg-open " + "\"" + args.filename + "\"")
            except RuntimeError:
                print('error: failed to play file')
    except FileNotFoundError:
        print('error: file is not found')
    except RuntimeError:
        print('error: file is corrupted by sin')

if __name__ == "__main__":
    main()
