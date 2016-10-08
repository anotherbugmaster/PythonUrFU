"""Tests"""
import unittest
import id3v1
import id3v2
import frame

class Test(unittest.TestCase):
    """Test class"""
    def setUp(self):
        self.mp3_info = {}
        self.mp3_info["v1"] = {}
        self.mp3_info["v2"] = {}
        self.mp3_info["frame"] = {}


        self.mp3_info["v1"]["1.mp3"] = {
            'Album': 'Meds (US Re-Release)',
            'Artist': 'Placebo',
            'Comment': '',
            'Genre': None,
            'Title': 'Meds (Feat. Alison Mosshart)',
            'Year': '2007'}
        self.mp3_info["v2"]["1.mp3"] = {
            'Lead performer(s)/Soloist(s)': 'Placebo',
            'Year': '2007',
            'Title/songname/content description': \
                'Meds (Feat. Alison Mosshart)',
            'Content type': 'Alternative Rock / Indie Rock',
            'Album/Movie/Show title': 'Meds (US Re-Release)',
            'Track number/Position in set': '1'}
        self.mp3_info["frame"]["1.mp3"] = {
            'Layer': 'Layer III',
            'Error Protection': 'Not protected',
            'Bit Rate': '320',
            'Version': 'MPEG',
            'Copyright': 'Not copyrighted',
            'Original': 'Original',
            'Mode': 'Joint stereo (Stereo)',
            'Frequency': '44100 Hz',
            'Size' : '6.73 Mb',
            'Length' : '2:56',
            'Frames amount': 6717}


        self.mp3_info["v1"]["2.mp3"] = {
            'Album': 'Рыба',
            'Artist': 'Ленинград',
            'Comment': 'Collected by Тарантиныч',
            'Genre': 'Rock',
            'Title': 'Вода',
            'Year': '2012'}
        self.mp3_info["v2"]["2.mp3"] = {
            'Lead performer(s)/Soloist(s)': 'Ленинград',
            'Recording time': '2012',
            'Title/songname/content description': \
                'Вода',
            'Comments' : 'Collected by Тарантиныч',
            'Content type': 'Rock',
            'Album/Movie/Show title': 'Рыба',
            'Track number/Position in set': '03/13',
            'User defined text information frame': \
                'FMPS_Rating_Amarok_Score0.94',
            'Popularimeter': '\x08',}
        self.mp3_info["frame"]["2.mp3"] = {
            'Layer': 'Layer III',
            'Error Protection': 'Not protected',
            'Bit Rate': '320',
            'Version': 'MPEG',
            'Copyright': 'Not copyrighted',
            'Original': 'Original',
            'Mode': 'Joint stereo (Stereo)',
            'Frequency': '44100 Hz',
            'Size' : '6.73 Mb',
            'Length' : '2:56',
            'Frames amount': 6717}


        self.mp3_info["v1"]["3.mp3"] = {}
        self.mp3_info["v1"]["4.mp3"] = {
            'Album': 'Consider The Birds',
            'Artist': 'Woven Hand',
            'Comment': '',
            'Genre': 'Rock',
            'Title': 'To Make A Ring',
            'Year': '2004'}
        self.mp3_info["v1"]["5.mp3"] = {
            'Album': 'Народные черноморские песни ку',
            'Artist': 'Кубанский Казачий Хор',
            'Comment': 'Виктор Захарченко - Музыкаль',
            'Genre': None,
            'Title': 'Плавай, плавай, лебедонько',
            'Year': '2008'}

    def test_id3v1(self):
        for key in self.mp3_info["v1"]:
            with self.subTest(key=key):
                res = id3v1.get_info(key)
                self.assertEqual(res, self.mp3_info["v1"][key])

    def test_id3v2(self):
        """ID3v2 info"""
        for key in self.mp3_info["v2"]:
            with self.subTest(key=key):
                res = id3v2.get_info(key)
                self.assertEqual(res, self.mp3_info["v2"][key])

    def test_frame_info(self):
        """Frame info"""
        for key in self.mp3_info["frame"]:
            with self.subTest(key=key):
                res = frame.get_info(key)
                self.assertEqual(res, self.mp3_info["frame"][key])

if __name__ == '__main__':
    unittest.main()
