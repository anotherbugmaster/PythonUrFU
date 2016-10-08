"""Mp3 frame parser"""
#usr/bin/python3

from id3v2 import get_tag_info_size
from id3v1 import is_id3v1_present
import os
from mp3_frame import Mp3FrameHeader
from itertools import islice

def get_info(filename):
    """Get info"""
    # headers = list(islice(get_headers(filename), 100))
    headers = list(get_headers(filename))
    header = headers[0]
    frame_info = {
        'Version': header.version,
        'Layer': header.layer,
        'Error Protection': header.error_prot,
        'Bit Rate': header.bit_rate,
        'Frequency': header.frequency,
        'Mode': header.mode,
        'Copyright': header.copyright,
        'Original': header.original,
        'Size': get_size(filename),
        'Length': get_length(filename, int(header.bit_rate)),
        'Frames amount': len(headers),
        }
    return frame_info

def get_headers(filename):
    """Get frame bits"""
    with open(filename, 'rb') as i_stream:
        file_bytes = i_stream.read()

        if file_bytes[:3] != b"ID3":
            id3v2_size = 0
        else:
            id3v2_size = get_tag_info_size(file_bytes[6:10])

        if is_id3v1_present(file_bytes):
            ending = len(file_bytes) -128
        else:
            ending = len(file_bytes)

        byte_number = id3v2_size
        while byte_number != ending:
            cur_bytes = file_bytes[byte_number:byte_number + 4]
            # print(byte_number)
            # print(cur_bytes)
            if is_header(cur_bytes):
                header = Mp3FrameHeader(cur_bytes)
                # print(header.header_bits)
                bit_rate = int(header.bit_rate)
                frequency = int(header.frequency[:-3])
                # print(bit_rate)
                padding = int(header.padding)
                frame_size = int((144 * bit_rate * 1000 / frequency) + padding)
                byte_number += frame_size
                yield header
            else:
                byte_number += 1

def is_header(bytes):
    or_mask = int.from_bytes(b'\x00\x0F', 'big')
    check_mask = int.from_bytes(b'\xFF\xFF', 'big')
    int_from_bytes = int.from_bytes(bytes[:2], 'big')
    is_sync = check_mask == (int_from_bytes | or_mask)

    int_from_bytes = int.from_bytes(bytes, 'big')

    bits = bin(int_from_bytes)[2:]
    layer_check = bits[13:15] != "00"
    bitrate_check = bits[16:20] != "1111" and bits[16:20] != "0000"
    sample_freq_check = bits[20:22] != "11"
    emphasis_check = bits[30:32] != "10"

    header_check = (
        is_sync and layer_check and bitrate_check and
        sample_freq_check and emphasis_check)

    return header_check

def get_size(filename):
    filesize = os.path.getsize(filename) / pow(2, 20)
    filesize = round(filesize, 2)
    return "%s Mb" % filesize

def get_length(filename, bitrate):
    filesize = os.path.getsize(filename) / pow(2, 20)
    seconds = int(filesize*1024*1024*8 // (bitrate*1000))

    return "%s:%s" % (seconds // 60, seconds % 60)
