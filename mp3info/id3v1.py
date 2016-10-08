"""ID3v1 parser"""
#usr/bin/python3

def get_info(filename):
    """Get info"""
    tag_bytes = get_tag_bytes(filename)
    if tag_bytes[:3] == b"TAG":
        try:
            tag_string = tag_bytes[:-1].decode("utf-16")
        except UnicodeDecodeError:
            try:
                tag_string = tag_bytes[:-1].decode("utf-8")
            except UnicodeDecodeError:
                tag_string = tag_bytes[:-1].decode("cp1251")
        genre_number = int.from_bytes(tag_bytes[-1:], "big")
        tag_info = {
            "Title": tag_string[3:33].strip('\x00'),
            "Artist": tag_string[33:63].strip('\x00'),
            "Album": tag_string[63:93].strip('\x00'),
            "Year": tag_string[93:97].strip('\x00'),
            "Comment": tag_string[97:126].strip('\x00'),
            "Genre": get_genre(genre_number),
        }
        return tag_info
    else:
        return dict()
    # TODO: variable encodings handling

def is_id3v1_present(bytes):
    return bytes[-128:-125] == b"TAG"

def get_tag_bytes(filename):
    """Get tag bytes"""
    with open(filename, 'rb') as i_stream:
        i_stream.seek(-128, 2)
        return i_stream.read(128)

def get_genre(genre_number):
    """Get genre"""
    try:
        with open("id3v1genres.db", 'r') as i_stream:
            lines = i_stream.read().splitlines()
            genres = {
                int(_.split(':')[0]) : _.split(':')[1] for _ in lines}
            if genre_number != 255:
                return genres[genre_number]
    except FileNotFoundError:
        print("error: file id3v1genres.db is not found")
