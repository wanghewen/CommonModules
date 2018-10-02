import unittest
import os

import CommonModules as CM

class TruthDownloadFile(unittest.TestCase):

    def test_download_file(self):
        CM.IO.DownloadFile("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                           Destination = "./download/test",
                           ExpectedBytes = 13264)
        CM.IO.RemoveDirectory("./download")

    def test_download_file_wrongsize(self):

        try:
            CM.IO.DownloadFile("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                               Destination = "./1.pdf",
                               ExpectedBytes=100)
        except FileExistsError:
            pass
        else:
            self.fail('Did not see FileExistsError')
        os.remove("./1.pdf")

if __name__ == '__main__':
    unittest.main()