"""
To manage a very large number of files (or key-value pairs) in a compressed archive
Assumptions: meta data is managed by user
"""

import os
import gzip
import pickle
from zipfile import ZipFile

class Archiver:
    archive_name = None
    key_value_dict = None
    mode = None
    active = None
    compression = None

    def __init__(self, full_path, mode, compression='zip', update=False, overwrite=False):
        assert mode == 'r' or mode == 'w'
        self.compression = compression
        self.archive_name = full_path
        self.mode = mode

        if mode == 'w':
            self.key_value_dict = {}
            if os.path.exists(full_path):
                if update:
                    self.load()
                elif overwrite:
                    os.remove(full_path)
                else:
                    raise RuntimeError(f'archive {full_path} already exists')
        else:
            if compression == 'zip':
                if not os.path.exists(full_path):
                    raise RuntimeError(f'archive {full_path} does not exist')
            else:
                if not os.path.exists(full_path):
                    raise RuntimeError(f'archive {full_path} does not exist')

            if compression == 'zip':
                self.key_value_dict = {}
                with ZipFile(full_path) as myzip:
                    for f in myzip.namelist():
                        self.key_value_dict[f] = myzip.read(f)
            elif compression == 'pickle':
                with gzip.open(full_path, 'rb') as f:
                    self.key_value_dict = pickle.load(f)
            else:
                assert False, f'Invalid compression: {compression}'

        self.active = True

    def add(self, key, data):
        if not self.active:
            assert False, f'Archive is in Inactive state'
        if self.mode == 'w' and self.active:
            self.key_value_dict[key] = data

    def get(self, key):
        if not self.active:
            assert False, f'Archive is in Inactive state'
        return self.key_value_dict[key] if (self.mode == 'r' and self.active) else None

    def size(self):
        if not self.active:
            assert False, f'Archive is in Inactive state'
        return len(self.key_value_dict) if self.active else None

    def keys(self):
        if not self.active:
            assert False, f'Archive is in Inactive state'
        return list(self.key_value_dict.keys())

    def flush(self, create_parent_dir=False):
        if self.active and self.mode == 'w':
            if create_parent_dir and not os.path.exists(os.path.dirname(self.archive_name)):
                os.mkdir(os.path.dirname(self.archive_name))
            if self.compression == 'zip':
                with ZipFile(self.archive_name, 'w') as myzip:
                    for f in list(self.key_value_dict.keys()):
                        myzip.writestr(f, self.key_value_dict[f])
            elif self.compression == 'pickle':
                with gzip.open(self.archive_name, 'wb') as f:
                    pickle.dump(self.key_value_dict, f)
            else:
                assert False, f'Invalid compression: {compression}'
            self.active = None
            self.archive_name = None
            self.key_value_dict = None
            self.mode = None
            self.compressed = None
        else:
            assert False, f'Archive is in Inactive state'

    def load(self):
        if self.compression == 'zip':
            self.key_value_dict = {}
            with ZipFile(self.archive_name) as myzip:
                for f in myzip.namelist():
                    self.key_value_dict[f] = myzip.read(f)
        elif self.compression == 'pickle':
            with gzip.open(self.archive_name, 'rb') as f:
                self.key_value_dict = pickle.load(f)
        else:
            assert False, f'Invalid compression: {compression}'
