"""
To manage a very large number of files (or key-value pairs) in a compressed archive
Assumptions: meta data is managed by user
"""

import os
import gzip
import pickle

LOG_DIR = os.path.join(os.getenv('HOME_DIR'), '98_log/pygeneric')

class Archiver:
    archive_name = None
    key_value_dict = None
    mode = None
    active = None
    compressed = None

    def __init__(self, full_path, mode, compressed=True, overwrite=False):
        assert mode == 'r' or mode == 'w'

        if mode == 'w':
            if os.path.exists(full_path):
                if overwrite:
                    os.remove(full_path)
                else:
                    raise RuntimeError(f'archive {full_path} already exists')
            self.key_value_dict = {}
        else:
            if not os.path.exists(full_path):
                raise RuntimeError(f'archive {full_path} does not exist')
            if compressed:
                with gzip.open(full_path, 'rb') as f:
                    self.key_value_dict = pickle.load(f)
            else:
                with open(full_path, 'rb') as f:
                    self.key_value_dict = pickle.load(f)

        self.compressed = compressed
        self.archive_name = full_path
        self.mode = mode
        self.active = True

    def add(self, key, data):
        if self.mode == 'w' and self.active:
            self.key_value_dict[key] = data

    def get(self, key):
        return self.key_value_dict[key] if (self.mode == 'r' and self.active) else None

    def size(self):
        return len(self.key_value_dict) if self.active else None

    def flush(self):
        if self.active and self.mode == 'w':
            if self.compressed:
                with gzip.open(self.archive_name, 'wb') as f:
                    pickle.dump(self.key_value_dict, f)
            else:
                with open(self.archive_name, 'wb') as f:
                    pickle.dump(self.key_value_dict, f)
            self.active = None
            self.archive_name = None
            self.key_value_dict = None
            self.mode = None
            self.compressed = None

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    archive_name = LOG_DIR + '/test_archive'
    ARCHIVE_SIZE = int(1e6)

    a1 = Archiver(archive_name, 'w', overwrite=True, compressed=True)
    for i in range(0, ARCHIVE_SIZE):
        a1.add(f'id_{i}', 100*f'{i}')
    a1.flush()
    print('Test 1: OK')

    try:
        a2 = Archiver(archive_name, 'w')
        print('THIS SHOULD NEVER BE PRINTED')
    except:
        print('Test 2: OK')

    a3 = Archiver(archive_name, 'r', compressed=True)
    assert a3.size() == ARCHIVE_SIZE, 'Test 3 failed'
    print('Test 3: OK')

    for i in range(1, ARCHIVE_SIZE):
        assert a3.get(f'id_{i}') == 100*f'{i}', 'Test 4 failed'

    print('Test 4: OK')

    try:
        a1 = Archiver(archive_name, 'w')
    except:
        print('Test 5: OK')

    print('All tests passed')