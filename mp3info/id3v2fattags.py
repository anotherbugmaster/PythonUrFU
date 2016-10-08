#!/usr/bin/python3

def COMM(bytes):
    print(bytes)
    encoding = bytes[:2]
    language = bytes[2:5]

    start = 5
    end = len(bytes) + 1
    for byte_index in range(start, len(bytes)):
        if bytes[byte_index] == b'\x00':
            end = byte_index
            break
    description = bytes[start:end]
    text = bytes[end + 1:]
    return {
        description : text
        }

dispatch = {
    b"COMM": COMM
}

