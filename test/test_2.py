import glob
import os
import pandas as pd
from archiver import Archiver
import io
import requests
from zipfile import ZipFile

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    LOG_DIR = os.path.join(os.getenv('HOME_DIR'), '98_log/pygeneric')
    archive_name = LOG_DIR + '/test_archive.zip'

    files1 = [
        'https://archives.nseindia.com/content/indices/ind_close_all_29092022.csv',
        'https://archives.nseindia.com/content/indices/ind_close_all_30092022.csv'
    ]
    a1 = Archiver(archive_name, 'w', overwrite=True, compression='zip')
    for f in files1:
        r = requests.get(f, headers=headers, stream=True)
        if r.ok:
            a1.add(os.path.basename(f), r.content)
    print(a1.keys())
    a1.flush()

    a2 = Archiver(archive_name, 'r', overwrite=True, compression='zip')
    print(a2.keys())
    for f in a2.keys():
        df = pd.read_csv(io.BytesIO(a2.get(f)))
    print(df.shape, list(df.columns))
    print('Test 1: OK\n')

    files2 = [
        'https://archives.nseindia.com/archives/equities/bhavcopy/pr/PR290922.zip',
        'https://archives.nseindia.com/archives/equities/bhavcopy/pr/PR300922.zip'
    ]

    a2 = Archiver(archive_name, 'w', overwrite=True, compression='zip')
    for f in files2:
        r = requests.get(f, headers=headers, stream=True)
        if r.ok:
            a2.add(os.path.basename(f), r.content)
    print(a2.keys())
    a2.flush()

    a2 = Archiver(archive_name, 'r', overwrite=True, compression='zip')
    print(a2.keys())
    for f in a2.keys():
        z = ZipFile(io.BytesIO(a2.get(f)))
        print(z.namelist())

    print('Done')