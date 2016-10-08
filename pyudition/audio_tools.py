"""Simple audio lib"""
#!/usr/bin/python3
import tkinter
import struct
import math
import wave
import os
import progress_bar
# import numpy as np


def gen_new_filename(filename):
    """Generates name for output file"""
    parts = filename.split('.')
    ext = "." + parts[len(parts) - 1]
    new_filename_base = '.'.join(parts[:-1]) + "_edited_"
    i = 1
    while True:
        new_filename = new_filename_base + str(i) + ext
        if not os.path.isfile(new_filename):
            return new_filename
        i += 1

def get_seconds(frame_i, framerate):
    """Convert frame_number to seconds"""
    return frame_i / framerate

def get_max_amp_abs(amplitudes):
    """Isn't it obvious enough?"""
    return max(
        max([abs(amp) for amp in amplitudes[0]]),
        max([abs(amp) for amp in amplitudes[1]]))

def to_amplitudes(wavefile):
    """Converts wavefile to amplitude array"""
    num_channels = wavefile.getnchannels()
    # sample_rate = wavefile.getframerate()
    sample_width = wavefile.getsampwidth()
    num_frames = wavefile.getnframes()

    raw_data = wavefile.readframes(num_frames)

    total_samples = num_frames * num_channels

    if sample_width == 1:
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    integer_data = struct.unpack(fmt, raw_data)
    del raw_data # Some memory optimization

    amplitudes = [[] for time in range(num_channels)]

    for index, value in enumerate(integer_data):
        bucket = index % num_channels
        amplitudes[bucket].append(value)

    return amplitudes


def to_wavefile(amplitudes, params, output_filename):
    """Converts amplitude array to wavefile"""
    print("Writing to file...")
    num_channels = len(amplitudes)
    num_amps = len(amplitudes[0])
    prog_bar = progress_bar.ProgressBar(num_channels*num_amps)
    buf_len = 5000000
    with wave.open(output_filename, 'w') as output_file:
        output_file.setparams(params)
        frames_buffer = []
        for j in range(num_amps):
            for i in range(num_channels):
                prog_bar.invoke(j*num_channels+i+1)
                amplitudes[i][j] = math.copysign(
                    min(32767, abs(amplitudes[i][j])),
                    amplitudes[i][j])
                amplitudes[i][j] = int(amplitudes[i][j])
                frames_buffer.append(struct.pack('h', amplitudes[i][j]))
            if j % buf_len == 0:
                output_file.writeframes(b''.join(frames_buffer))
                frames_buffer = []
        output_file.writeframes(b''.join(frames_buffer))

    return output_filename


def normalize(amplitudes, percent):
    """Sets normalization coefficient"""
    num_channels = len(amplitudes)
    num_amps = len(amplitudes[0])
    prog_bar = progress_bar.ProgressBar(num_channels*num_amps)
    for i in range(num_channels):
        for j in range(num_amps):
            amplitudes[i][j] = math.floor(amplitudes[i][j] * (percent/100))

            prog_bar.invoke(i*num_amps+j+1)


def compression(amplitudes, level):
    """Makes too loud sounds quiter"""
    num_channels = len(amplitudes)
    num_amps = len(amplitudes[0])
    prog_bar = progress_bar.ProgressBar(num_channels*num_amps)
    for i in range(num_channels):
        for j in range(num_amps):
            amp = abs(amplitudes[i][j])
            if amp > level:
                amplitudes[i][j] = int(math.copysign(level, amplitudes[i][j]))

            prog_bar.invoke(i*num_amps+j+1)

def noise_reduction(amplitudes, level):
    """Removes unwanted low-volume noises"""
    num_channels = len(amplitudes)
    num_amps = len(amplitudes[0])
    prog_bar = progress_bar.ProgressBar(num_channels*num_amps)
    for i in range(num_channels):
        for j in range(num_amps):
            amp = abs(amplitudes[i][j])
            if amp < level:
                amplitudes[i][j] = 0

            prog_bar.invoke(i*num_amps+j+1)


def stretch(output_filename, params, percent):
    """Changes duration of wavefile"""
    with wave.open(output_filename, 'w') as output_file:
        output_file.setparams(params)
        output_file.setframerate(params.framerate * percent * 0.01)


def merge(amps1, amps2):
    """Merges two files into one"""
    num_channels = max(len(amps1), len(amps2))
    if len(amps1) < len(amps2):
        amps1.append(0 for amp in amps1[0])
    elif len(amps1) > len(amps2):
        amps2.append(0 for amp in amps2[0])
    prog_bar = progress_bar.ProgressBar(num_channels)
    for i in range(num_channels):
        amps1[i] += amps2[i]
        prog_bar.invoke(i+1)
    return amps1


def split(amplitudes, time, framerate):
    """Split file by given index"""
    num_channels = len(amplitudes)
    amps1 = []
    amps2 = []
    index = int(framerate * time)
    if index <= 0 or index >= len(amplitudes[0]) - 1:
        print("Error: inappropriate time value.")
        exit()
    prog_bar = progress_bar.ProgressBar(num_channels)
    for i in range(num_channels):
        amps1.append(amplitudes[i][:index])
        amps2.append(amplitudes[i][index:])
        prog_bar.invoke(i+1)
    return (amps1, amps2)


# def time_stretch(amps, f, window_size, h):
#     amps1 =

#     for amp in amps:
#         phase = np.zeros(window_size)
#         hanning_window = np.hanning(window_size)
#         result = np.zeros(len(amp) /f + window_size)

#         for i in np.arrange(0, len(amp) - (window_size + h), h*f):

#             a1 = amp[i: i + window_size]
#             a2 = amp[i + h: i + window_size + h]

#             s1 = np.fft.fft(hanning_window * a1)
#             s2 = np.fft.fft(hanning_window * a2)
#             phase = (phase + np.angle(s2/s1)) % 2*np.pi
#             a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

#             i2 = int(i/f)
#             result[i2 : i2 + window_size] += hanning_window*a2_rephased

#         result = ((2**(16 - 4)) * result/result.max())

#     return result.astype('int16')


def pitch_shift():
    """Changes pitch of wavefile"""
    pass

def play(wavefile):
    """Play file through OS default player"""
    os.system("\""+wavefile+"\"")


def overlapse(amps1, amps2, time, framerate):
    """Overlapping two files"""
    num_channels = max(len(amps1), len(amps2))
    frame_index = int(time * framerate)
    if frame_index < 0:
        print("Error: inappropriate time value.")
        exit()

    if len(amps1) < len(amps2):
        amps1.append(0 for amp in amps1[0])
    elif len(amps1) > len(amps2):
        amps2.append(0 for amp in amps2[0])

    for i in range(num_channels):
        for j in range(len(amps2[i]) - len(amps1[i]) + frame_index):
            amps1[i].append(0)
    # TODO: Remake progress bar
    prog_bar = progress_bar.ProgressBar(num_channels)
    for i in range(num_channels):
        prog_bar.invoke(i + 1)
        for j in range(len(amps2[0])):
            amps1[i][frame_index + j] += amps2[i][j]
    return amps1


def info(wavefile):
    """Print audio metadata"""
    with wave.open(wavefile, 'r') as wavefile:
        params = wavefile.getparams()
        amps = to_amplitudes(wavefile)
        print("Number of channels: %s" % params.nchannels)
        print("Sample width: %s" % params.sampwidth)
        print("Framerate: %s" % params.framerate)
        print("Number of frames: %s" % params.nframes)
        print("Length: %s seconds" % int(params.nframes / params.framerate))
        print("Max amplitude's modulus: %s" % get_max_amp_abs(amps))
        print("Compression name: %s" % params.compname)


def draw_histogram(amplitudes):
    """Draws pretty histogram based on wavefile"""
    window = tkinter.Tk()
    window.title('AnotherBugAudio')

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()

    canvas = tkinter.Canvas(window,
                            width=width,
                            height=height,
                            background="black")

    channels_amount = len(amplitudes)
    chunk_size = int(len(amplitudes[0]) / width)
    for channel in range(channels_amount):
        for i in range(width):
            average_amplitude = 0
            for amp in amplitudes[channel][i*chunk_size:(i+1)*(chunk_size)]:
                average_amplitude = max(average_amplitude, abs(amp))
                if amp < 0:
                    average_amplitude *= -1
            line_height = average_amplitude / 50
            line_end_1 = height/4 if channel == 0 else height*3/4
            line_end_2 = (
                (height/4 if channel == 0 else height*3/4)
                + line_height)
            canvas.create_line(min(i, width), line_end_1,
                               min(i, width), line_end_2,
                               fill=("green" if channel == 0 else "blue"))

    canvas.pack()
    tkinter.mainloop()

# draw_histogram(amplitudes)
