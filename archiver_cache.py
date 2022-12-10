"""
Efficient reading of large number of large size archive files. Using n-size cache
Assumptions: meta data is managed by user. Expects a function to map key to archive_path
"""
''' --------------------------------------------------------------------------------------- '''
import pygeneric.archiver as archiver

''' --------------------------------------------------------------------------------------- '''
class ArchiverCache:
    def __init__(self, archive_path_func, cache_size=5, verbose=False):
        assert archive_path_func is not None, 'ERROR! archive_path_func is None'
        assert cache_size > 1, 'ERROR! cache_size is %d' % cache_size

        self.archive_dict = {}
        self.archive_path_func = archive_path_func
        self.cache_size = cache_size

        self.n_loaded = 0
        self.n_get_value_calls = 0

        self.verbose = verbose
        if self.verbose:
            print('ArchiverCache: cache_size/%d initialized' % self.cache_size)
        self.status = True

    def all_ok(self):
        return self.status

    def get_value(self, key):
        assert len(self.archive_dict.keys()) <= self.cache_size,\
            'cache size exceeded limit: %d/%d' % (len(self.archive_dict.keys()), self.cache_size)

        self.n_get_value_calls += 1
        archive_path = self.archive_path_func(key)
        if archive_path not in self.archive_dict.keys():
            if len(self.archive_dict.keys()) >= self.cache_size:
                self.archive_dict.pop(list(self.archive_dict.keys())[0])
            self.archive_dict[archive_path] = archiver.Archiver(archive_path, mode='r')
            self.n_loaded += 1
            if self.verbose:
                print('\nLoaded new archive into cache')

        if self.verbose and self.n_get_value_calls % 5 == 0:
            print('\nArchiverCache efficiency: %d/%d/%.2f'
                  % (self.n_get_value_calls, self.n_loaded, self.n_get_value_calls/self.n_loaded))

        return self.archive_dict[archive_path].get(key)