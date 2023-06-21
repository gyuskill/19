import unittest
from unittest.mock import patch, mock_open
from nw_diff import get_scp_back_dir, get_scp_back_date, get_file_date

class TestYourModule(unittest.TestCase):

    @patch("os.listdir")
    def test_get_scp_back_dir(self, mock_listdir):
        mock_listdir.return_value = ['not_scp_backup_from-', 'scp_backup_from-1', 'scp_backup_from-2']
        result = get_scp_back_dir('/path/to/dir')
        self.assertEqual(result, ['scp_backup_from-1', 'scp_backup_from-2'])

    @patch("os.listdir")
    def test_get_scp_back_date(self, mock_listdir):
        mock_listdir.return_value = ['file-running-config-20230101_01', 'file-running-config-20230102_02']
        result = get_scp_back_date('/path/to/dir')
        self.assertEqual(result, ['20230101', '20230102'])

    def test_get_file_date(self):
        result = get_file_date('file-running-config-20230101_010203')
        self.assertEqual(result, datetime.datetime(2023, 1, 1, 1, 2, 3))


if __name__ == '__main__':
    unittest.main()
