#!/usr/bin/python3
"""Main interface module"""

import argparse
import audio_tools
import wave
import os

class PyuditionUI():
    """Parsers"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="""Simple audio tool. Tested only on Windows.""")
        subparsers = self.parser.add_subparsers(
            dest="command",
            metavar="command")

        parser_norm = subparsers.add_parser(
            'norm',
            aliases=["n"],
            help="Normalize")
        parser_norm.add_argument("input", help="Input")
        parser_norm.add_argument(
            "percent",
            type=int,
            default=100,
            help="Volume in percents")
        parser_norm.add_argument("output", help="Output")
        parser_norm.set_defaults(func=self.norm)

        parser_comp = subparsers.add_parser(
            'comp',
            aliases=["c"],
            help="Compress")
        parser_comp.add_argument("input", help="Input")
        parser_comp.add_argument(
            "level",
            type=int,
            default=100,
            help="Volume level (0, 32767)")
        parser_comp.add_argument("output", help="Output")
        parser_comp.set_defaults(func=self.comp)

        parser_nred = subparsers.add_parser(
            'nred',
            aliases=["nr"],
            help="Noise reduction")
        parser_nred.add_argument("input", help="Input")
        parser_nred.add_argument(
            "level",
            type=int,
            default=100,
            help="Volume level (0, 32767)")
        parser_nred.add_argument("output", help="Output")
        parser_nred.set_defaults(func=self.nred)

        parser_merge = subparsers.add_parser(
            'merge',
            aliases=["m"],
            help="Merge")
        parser_merge.add_argument(
            "input1",
            help="Input1")
        parser_merge.add_argument(
            "input2",
            help="Input2")
        #TODO: Add list of files to merge
        parser_merge.add_argument("output", help="Output")
        parser_merge.set_defaults(func=self.merge)

        parser_olap = subparsers.add_parser(
            'olap',
            aliases=["o"],
            help="Overlapping")
        parser_olap.add_argument(
            "input1",
            help="Input1")
        parser_olap.add_argument(
            "input2",
            help="Input2")
        parser_olap.add_argument(
            "time",
            type=float,
            default=0,
            help="""Time in seconds where to start playing second file""")
        parser_olap.add_argument("output", help="Output")
        parser_olap.set_defaults(func=self.olap)

        parser_split = subparsers.add_parser(
            'split',
            aliases=["sp"],
            help="Split")
        parser_split.add_argument("input", help="Input")
        parser_split.add_argument(
            "time",
            type=float,
            default=0,
            help="Time in seconds where to split")
        parser_split.add_argument("output1", help="Output1")
        #TODO: split to many pieces
        parser_split.add_argument("output2", help="Output2")
        parser_split.set_defaults(func=self.split)

        parser_stretch = subparsers.add_parser(
            'stretch',
            aliases=["st"],
            help="Stretch")
        parser_stretch.add_argument("input", help="Input")
        parser_stretch.add_argument(
            "percent",
            type=float,
            default=100,
            help="Stretch percent")
        parser_stretch.add_argument("output", help="Output")
        parser_stretch.set_defaults(func=self.stretch)

        # parser_pitch = subparsers.add_parser(
        #     'pitch',
        #     aliases=["pt"],
        #     help="Pitch")
        # parser_pitch.add_argument("input", help="Input")
        # parser_pitch.add_argument(
        #     "level",
        #     help="Pitch level")
        # parser_pitch.add_argument("output", help="Output")
        # parser_pitch.set_defaults(func=self.pitch)

        parser_play = subparsers.add_parser(
            'play',
            aliases=["p"],
            help="Play file")
        parser_play.add_argument("input", help="Input")
        parser_play.set_defaults(func=self.play)

        parser_batch = subparsers.add_parser(
            'batch',
            aliases=["b"],
            help="Batch mode")
        parser_batch.add_argument("input")
        parser_batch.set_defaults(func=self.batch)

        parser_info = subparsers.add_parser(
            'info',
            aliases=["i"],
            help="Show metadata")
        parser_info.add_argument("input")
        parser_info.set_defaults(func=self.info)

        args = self.parser.parse_args()
        if args.command == None:
            self.parser.error('''the following arguments are required: command.
Please use -h key to see help''')
        else:
            args.func(args)

        print('\n')

    def norm(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Normalizing...")
        with wave.open(args.input, 'r') as input_file:
            params = input_file.getparams()
            amplitudes = audio_tools.to_amplitudes(input_file)
        audio_tools.normalize(amplitudes, args.percent)
        audio_tools.to_wavefile(amplitudes, params, args.output)

    def comp(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Compression...")
        with wave.open(args.input, 'r') as input_file:
            params = input_file.getparams()
            amplitudes = audio_tools.to_amplitudes(input_file)
        audio_tools.compression(amplitudes, args.level)
        audio_tools.to_wavefile(amplitudes, params, args.output)

    def nred(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Noise reduction...")
        with wave.open(args.input, 'r') as input_file:
            params = input_file.getparams()
            amplitudes = audio_tools.to_amplitudes(input_file)
        audio_tools.noise_reduction(amplitudes, args.level)
        audio_tools.to_wavefile(amplitudes, params, args.output)

    def merge(self, args):
        if not os.path.isfile(args.input1):
            self.parser.error('''wrong file: ''' + args.input1)
        elif not os.path.isfile(args.input2):
            self.parser.error('''wrong file: ''' + args.input2)

        print("Merging...")
        with wave.open(args.input1, 'r') as input_file:
            params = input_file.getparams()
            amps1 = audio_tools.to_amplitudes(input_file)

        with wave.open(args.input2, 'r') as input_file:
            amps2 = audio_tools.to_amplitudes(input_file)

        amplitudes = audio_tools.merge(amps1, amps2)
        audio_tools.to_wavefile(amplitudes, params, args.output)

    def olap(self, args):
        if not os.path.isfile(args.input1):
            self.parser.error('''wrong file: ''' + args.input1)
        elif not os.path.isfile(args.input2):
            self.parser.error('''wrong file: ''' + args.input2)

        print("Overlapping...")
        with wave.open(args.input1, 'r') as input_file:
            params = input_file.getparams()
            amps1 = audio_tools.to_amplitudes(input_file)

        with wave.open(args.input2, 'r') as input_file:
            amps2 = audio_tools.to_amplitudes(input_file)

        amplitudes = audio_tools.overlapse(
            amps1,
            amps2,
            args.time,
            params.framerate)
        audio_tools.to_wavefile(amplitudes, params, args.output)

    def split(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Splitting...")
        with wave.open(args.input, 'r') as input_file:
            params = input_file.getparams()
            amplitudes = audio_tools.to_amplitudes(input_file)

        ampses = audio_tools.split(amplitudes, args.time, params.framerate)
        audio_tools.to_wavefile(ampses[0], params, args.output1)
        audio_tools.to_wavefile(ampses[1], params, args.output2)


    def stretch(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Stretching...")
        with wave.open(args.input, 'r') as input_file:
            params = input_file.getparams()
            amplitudes = audio_tools.to_amplitudes(input_file)

        params_mod = (params.nchannels, params.sampwidth,
                      params.framerate * args.percent * 0.01,
                      params.nframes, params.comptype, params.compname)
        audio_tools.to_wavefile(amplitudes, params_mod, args.output)
        # audio_tools.stretch(args.output, params, args.percent)


    def pitch(args):
        print("Pitching...")


    def batch(self, args):
        if not os.path.isfile(args.input):
            self.parser.error('''wrong file: ''' + args.input)

        with open(args.input, 'r') as input_file:
            lines = input_file.readlines()
        for line in lines:
            file_args = self.parser.parse_args(line.split())
            if file_args.command == None:
                self.parser.error('''
the following arguments are required: command.
Please use -h key to see help''')
            else:
                file_args.func(file_args)



    def info(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("INFO:")
        audio_tools.info(args.input)


    def play(self, args):
        if not os.path.isfile(args.input) or args.input[-3:] != "wav":
            self.parser.error('''wrong file: ''' + args.input)

        print("Playing...")
        audio_tools.play(args.input)

if __name__ == "__main__":
    PyuditionUI()
