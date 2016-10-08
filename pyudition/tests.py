#!/usr/bin/python3

import unittest
import wave
import audio_tools
import os
import math
import struct
import itertools

class TestPyudition(unittest.TestCase):
    def create_test_audio(self, frequency, amplitude):
        filename = audio_tools.gen_new_filename("temp.wav")
        framerate = 48000
        input_file = wave.open(filename, 'w')
        input_file.setnchannels(1)
        input_file.setsampwidth(2)
        input_file.setframerate(framerate)
        input_file.setnframes(framerate)
        for i in range(framerate):
            value = amplitude * math.sin(i / framerate * frequency)
            input_file.writeframes(struct.pack('h', int(value)))
        input_file.close()
        return filename

    def test_normalize(self):
        """Normalization test"""
        tempfile = self.create_test_audio(500, 2000)
        input_file = wave.open(tempfile, 'r')
        amps = audio_tools.to_amplitudes(input_file)
        input_file.close()
        sum1 = sum(itertools.chain.from_iterable(amps))
        audio_tools.normalize(amps, 200)
        sum2 = sum(itertools.chain.from_iterable(amps))
        self.assertEqual(2*sum1, sum2)
        os.remove(tempfile)

    def test_compression(self):
        """Compression test"""
        tempfile = self.create_test_audio(500, 2000)
        input_file = wave.open(tempfile, 'r')
        amps = audio_tools.to_amplitudes(input_file)
        input_file.close()
        audio_tools.compression(amps, 200)
        max1 = max(itertools.chain.from_iterable(amps))
        self.assertEqual(max1, 200)
        os.remove(tempfile)

    def test_overlapse(self):
        """Overlapping test"""
        tempfile1 = self.create_test_audio(500, 2000)
        tempfile2 = self.create_test_audio(500, 2000)
        input_file1 = wave.open(tempfile1, 'r')
        input_file2 = wave.open(tempfile2, 'r')
        amps1 = audio_tools.to_amplitudes(input_file1)
        amps2 = audio_tools.to_amplitudes(input_file2)
        input_file1.close()
        input_file2.close()
        audio_tools.overlapse(amps1, amps2, 5, 500)
        self.assertEqual(len(amps1[0]), len(amps2[0]) + 2500)
        os.remove(tempfile1)
        os.remove(tempfile2)

    def test_merge(self):
        """Merging test"""
        tempfile1 = self.create_test_audio(500, 2000)
        tempfile2 = self.create_test_audio(500, 2000)
        input_file1 = wave.open(tempfile1, 'r')
        input_file2 = wave.open(tempfile2, 'r')
        amps1 = audio_tools.to_amplitudes(input_file1)
        amps2 = audio_tools.to_amplitudes(input_file2)
        input_file1.close()
        input_file2.close()
        len1 = len(amps1[0])
        audio_tools.merge(amps1, amps2)
        len2 = len(amps1[0])
        self.assertEqual(len2, len1 + len(amps2[0]))
        os.remove(tempfile1)
        os.remove(tempfile2)

    def test_split(self):
        """Splitting test"""
        tempfile = self.create_test_audio(500, 2000)
        input_file = wave.open(tempfile, 'r')
        amps = audio_tools.to_amplitudes(input_file)
        input_file.close()
        amps1, amps2 = audio_tools.split(amps, 5, 500)
        self.assertEqual(len(amps1[0]) + len(amps2[0]), len(amps[0]))
        os.remove(tempfile)

    def test_noise_reduction(self):
        """Noise reduction test"""
        tempfile = self.create_test_audio(500, 2000)
        input_file = wave.open(tempfile, 'r')
        amps = audio_tools.to_amplitudes(input_file)
        input_file.close()
        audio_tools.noise_reduction(amps, 200)
        min1 = min(abs(x) for x in \
            itertools.chain.from_iterable(amps) if x != 0)
        self.assertEqual(min1, 200)
        os.remove(tempfile)

if __name__ == "__main__":
    unittest.main()
