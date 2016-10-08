#!/usr/bin/python3

class Mp3Frame():
    def __init__(self, frame_bytes):
        self.header = Mp3FrameHeader(frame_bytes[:4])
        self.data = frame_bytes[4:]

class Mp3FrameHeader():
    def __init__(self, bytes):

        def to_bit_array(bytes):
            int_from_bytes = int.from_bytes(bytes, 'big')
            return bin(int_from_bytes)[2:]

        self.header_bits = to_bit_array(bytes)
        # print(self.header_bits)
        self.version = self.get_version()
        self.layer = self.get_layer()
        self.error_prot = self.get_error_prot()
        self.bit_rate = self.get_bit_rate()
        self.frequency = self.get_frequency()
        self.mode = self.get_mode()
        self.padding = self.get_padding()
        self.copyright = self.get_copyright()
        self.original = self.get_original()

    def get_version(self):
        """Get version"""
        variants = {
            "0":"Not MPEG",
            "1":"MPEG"}
        return variants[self.header_bits[12]]

    def get_layer(self):
        """Get layer"""
        variants = {
            "00":"Reserved",
            "01":"Layer III",
            "10":"Layer II",
            "11":"Layer I"}
        return variants[self.header_bits[13:15]]

    def get_error_prot(self):
        """Get error bit"""
        variants = {
            "0":"Protected by CRC (16bit crc follows header)",
            "1":"Not protected"}
        return variants[self.header_bits[15:16]]

    def get_bit_rate(self):
        """Get bit rate"""
        variants = {
            "0000": "Free",
            "0001": "32",
            "0010": "40",
            "0011": "48",
            "0100": "56",
            "0101": "64",
            "0110": "80",
            "0111": "96",
            "1000": "112",
            "1001": "128",
            "1010": "160",
            "1011": "192",
            "1100": "224",
            "1101": "256",
            "1110": "320"}
        return variants[self.header_bits[16:20]]

    def get_frequency(self):
        """Get frequency"""
        variants = {
            "00":"44100 Hz",
            "01":"48000 Hz",
            "10":"32000 Hz",
            "11":"Reserved"}
        return variants[self.header_bits[20:22]]
    def get_padding(self):
        """Get frequency"""
        variants = {
            "0":"0",
            "1":"1"}
        return variants[self.header_bits[22]]

    def get_mode(self):
        """Get mode"""
        variants = {
            "00":"Stereo",
            "01":"Joint stereo (Stereo)",
            "10":"Dual channel (2 mono channels)",
            "11":"Single channel (Mono)"}
        return variants[self.header_bits[24:26]]

    def get_copyright(self):
        """Get copyright"""
        variants = {
            "0":"Not copyrighted",
            "1":"Copyrighted"}
        return variants[self.header_bits[28]]

    def get_original(self):
        """Get original"""
        variants = {
            "0":"Copy",
            "1":"Original"}
        return variants[self.header_bits[29]]
