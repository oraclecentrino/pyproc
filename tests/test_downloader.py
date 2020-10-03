import unittest
from scripts.downloader import *

class DownloaderTest(unittest.TestCase):

    def test_context_parser(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--keyword WKWK --tahun-anggaran 2020 --chunk-size 1000 --workers 999 --timeout 99 "
                                 "--non-tender --index-download-delay 5 --keep-workdir --force --clear "
                                 "https://lpse.sumbarprov.go.id".split(' '))
        expected_condition = {'keyword': 'WKWK', 'tahun_anggaran': [2020], 'chunk_size': 1000, 'workers': 999,
                              'timeout': 99, 'non_tender': True, 'index_download_delay': 5, 'keep_workdir': True,
                              'force': True, 'clear': True,
                              '_DownloaderContext__lpse_host': 'https://lpse.sumbarprov.go.id'}
        self.assertEqual(ctx.__dict__, expected_condition)

    def test_tahun_anggaran_parser_single_tahun(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--tahun-anggaran 2015 https://lpse.sumbarprov.go.id".split(' '))
        self.assertEqual([2015], ctx.tahun_anggaran)

    def test_tahun_anggaran_parser_multiple_tahun(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--tahun-anggaran 2015,2016,2020 https://lpse.sumbarprov.go.id".split(' '))
        self.assertEqual([2015, 2016, 2020], ctx.tahun_anggaran)

    def test_tahun_anggaran_parser_range_tahun(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--tahun-anggaran 2015-2020 https://lpse.sumbarprov.go.id".split(' '))
        self.assertEqual([i for i in range(2015,2021)], ctx.tahun_anggaran)

    def test_tahun_anggaran_parser_range_and_multiple_tahun(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--tahun-anggaran 2015-2020,2013,2012 https://lpse.sumbarprov.go.id".split(' '))
        self.assertEqual([2012, 2013, 2015, 2016, 2017, 2018, 2019, 2020], ctx.tahun_anggaran)

    def test_tahun_anggaran_parser_invalid_format_1(self):
        downloader = Downloader()
        self.assertRaises(DownloaderContextException, downloader.get_ctx,
                          "--tahun-anggaran 2015;2020 https://lpse.sumbarprov.go.id".split(' '))

    def test_tahun_anggaran_parser_invalid_value(self):
        downloader = Downloader()
        self.assertRaises(DownloaderContextException, downloader.get_ctx,
                          "--tahun-anggaran 1999-2030 https://lpse.sumbarprov.go.id".split(' '))

    def test_lpse_host_parser(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG http://lpse.sumbarprov.go.id".split(' '))

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertEqual('http://lpse.sumbarprov.go.id', i.url)
            self.assertEqual('http_lpse_sumbarprov_go_id.csv', i.filename.name)

    def test_lpse_host_multiple(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG http://lpse.sumbarprov.go.id,https://lpse.bengkuluprov.go.id".split(' '))
        urls = ['http://lpse.sumbarprov.go.id', 'https://lpse.bengkuluprov.go.id']
        filename = ['http_lpse_sumbarprov_go_id.csv', 'https_lpse_bengkuluprov_go_id.csv']

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertTrue(i.url in urls and i.filename.name in filename)

    def test_lpse_host_single_with_filename(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG http://lpse.sumbarprov.go.id;hasil-sumbarprov.csv".split(' '))

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertEqual('http://lpse.sumbarprov.go.id', i.url)
            self.assertEqual('hasil-sumbarprov.csv', i.filename.name)

    def test_lpse_host_multiple_with_filename(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG http://lpse.sumbarprov.go.id;sumbar.csv,https://lpse.bengkuluprov.go.id;bengkulu.csv".split(' '))
        urls = ['http://lpse.sumbarprov.go.id', 'https://lpse.bengkuluprov.go.id']
        filename = ['sumbar.csv', 'bengkulu.csv']

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertTrue(i.url in urls and i.filename.name in filename)

    def test_lpse_host_from_file(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG supporting_files/list-host.txt".split(' '))
        urls = ['http://lpse.sumbarprov.go.id', 'http://lpse.bengkuluprov.go.id']
        filename = ['http_lpse_sumbarprov_go_id.csv', 'http_lpse_bengkuluprov_go_id.csv']

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertTrue(i.url in urls and i.filename.name in filename)

    def test_lpse_host_from_file_multiple_with_filename(self):
        downloader = Downloader()
        ctx = downloader.get_ctx("--log=DEBUG supporting_files/list-host-with-filename.txt".split(' '))
        urls = ['http://lpse.sumbarprov.go.id', 'http://lpse.bengkuluprov.go.id']
        filename = ['sumbar.csv', 'bengkulu.csv']

        for i in ctx.lpse_host:
            self.assertTrue(i.is_valid)
            self.assertIsNone(i.error)
            self.assertTrue(i.url in urls and i.filename.name in filename)