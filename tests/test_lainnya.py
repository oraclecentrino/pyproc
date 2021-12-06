import unittest
from pyproc.lpse import Lpse, LpseDetilPencatatan


class TestLainnya(unittest.TestCase):

    def test_pencatatan_non_tender(self):
        self.lpse = Lpse('lpse.jakarta.go.id')
        nonspk = self.lpse.get_pencatatan_non_tender(start=0, length=5)
        self.assertTrue(len(nonspk['data']) == 5)

    def test_pencatatan_swakelola(self):
        self.lpse = Lpse('lpse.jakarta.go.id')
        swakelola = self.lpse.get_pencatatan_swakelola(start=0, length=5)
        self.assertTrue(len(swakelola['data']) == 5)

    def test_pencatatan_pengadaan_darurat(self):
        self.lpse = Lpse('lpse.jabarprov.go.id')
        darurat = self.lpse.get_pencatatan_pengadaan_darurat(start=0, length=5)
        print(darurat)

    def test_get_detail_pencatatan_non_tender(self):
        lpse = Lpse('lpse.jabarprov.go.id')
        nonspk = lpse.get_pencatatan_non_tender(start=0, length=1, data_only=True)
        detil = LpseDetilPencatatan(
            tipe_pencatatan='pencatatan_non_tender',
            lpse=lpse,
            id_paket=nonspk[0][0]
        )
        print(detil.get_detil())


if __name__ == '__main__':
    unittest.main()
