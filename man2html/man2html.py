#!/usr/bin/python3
""".man to .html converter"""

import argparse
import tarfile
import os
from converter import Converter

def main():
    """Main loop"""
    parser = argparse.ArgumentParser(".man to .html converter")
    parser.add_argument("input")
    parser.add_argument("output", nargs="?")
    parser.add_argument("--style", "-s", nargs="?", const="stylesheet.css")
    parser.add_argument("--tar", "-t", action="store_true")
    args = parser.parse_args()
    if not args.tar:
        convert_file(args)
    else:
        convert_tar(args)

def convert_file(args):
    if not args.output:
        args.output = args.input + ".html"
    with open(args.input, "r") as i_stream:
        with open(args.output, "w+") as o_stream:
            man_text = i_stream.readlines()
            html_text = Converter(man_text, args.style).convert()
            o_stream.writelines(html_text)

def convert_tar(args):
    if not args.output:
        args.output = args.input + ".html"
    if not os.path.isfile(args.input) or not tarfile.is_tarfile(args.input):
        print('Incorrect path to file')
        quit()
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    tar = tarfile.open(args.input)
    members = tar.getmembers()
    for member in members:
        with open(args.output + "/" + member.name + ".html", "w+") as o_stream:
            f = tar.extractfile(member)
            man_text = f.readlines()
            html_text = Converter(man_text, args.style).convert()
            o_stream.writelines(html_text)

if __name__ == '__main__':
    main()
