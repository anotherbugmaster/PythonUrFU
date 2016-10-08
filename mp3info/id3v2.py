"""ID3v2 parser"""
#!usr/bin/python3

H_SIZE = 10

from id3v2fattags import dispatch
import chardet

def get_info(filename):
    """Get info"""
    tag_info = {}
    tag_bytes = get_tag_bytes(filename)
    tags = load_tags()
    if tag_bytes[:3] == b"ID3":
        tag_info_size = get_tag_info_size(tag_bytes[6:10])
        offset = H_SIZE
        tag_bytes = tag_bytes[:tag_info_size + offset]
        for _ in range(tag_info_size, 0, -1):
            frame_id = tag_bytes[offset:offset + 4]
            if frame_id in tags:
                frame_size = int.from_bytes(
                    tag_bytes[offset + 4:offset + 8],
                    'big')
                frame_data = tag_bytes[offset + 11:offset + 10 + frame_size]
                if frame_id == b'APIC':
                    for byte_index, _ in enumerate(frame_data):
                        if frame_data[byte_index:byte_index + 3] == b'\xff\xd8\xff':
                            frame_data = frame_data[byte_index:]
                            break
                    with open('cover.jpg', 'wb+') as o_stream:
                        o_stream.write(frame_data)
                else:
                    if frame_id == b'COMM' or frame_id == b'USLT':
                        frame_data = frame_data[3:]
                    # if frame_id in dispatch:
                    #     tag_dict = dispatch[frame_id](frame_data)
                    #     print(tag_dict)
                    # else:
                    frame_data = frame_data.replace(b"\x00", b"").strip()
                    frame_data = frame_data.replace(b"\xff\xfe", b"").strip()
                    try:
                        enc = chardet.detect(frame_data)["encoding"]
                        # print(enc)
                        tag_info[tags[frame_id]] = frame_data.decode(enc)
                    except (UnicodeDecodeError, TypeError):
                        try:
                            tag_info[tags[frame_id]] = frame_data.decode("utf-16")
                        except UnicodeDecodeError:
                            try:
                                tag_info[tags[frame_id]] = frame_data.decode("utf-8")
                            except UnicodeDecodeError:
                                tag_info[tags[frame_id]] = frame_data.decode("cp1251")

            offset += H_SIZE + frame_size
        return tag_info
    else:
        return dict()

def get_tag_bytes(filename):
    """Get tag bytes"""
    with open(filename, 'rb') as i_stream:
        return i_stream.read()

def load_tags():
    """Load tags"""
    try:
        with open("id3v2tags.db", 'r') as i_stream:
            lines = i_stream.read().splitlines()
            tags = {
                str.encode(_.split(':')[0]) : _.split(':')[1] for _ in lines}
            return tags
    except FileNotFoundError:
        print("error: file id3v2tags.db is not found")

def get_tag_info_size(bytes):
    """Get tag info size"""
    tag_info_size = 10
    for byte_number in range(4):
        current_number = int(
            bytes[byte_number]) * pow(128, 3 - byte_number)
        tag_info_size += current_number
    return tag_info_size
