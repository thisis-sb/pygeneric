import os
from archiver import Archiver

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    LOG_DIR = os.path.join(os.getenv('HOME_DIR'), '98_log/pygeneric')
    archive_name = LOG_DIR + '/test_archive.zip'
    ARCHIVE_SIZE = int(1000)
    FILE_SIZE    = 10000

    a1 = Archiver(archive_name, 'w', overwrite=True)
    for i in range(0, ARCHIVE_SIZE):
        a1.add(f'id_{i}', bytes(FILE_SIZE*f'{i}', 'utf-8'))
    a1.flush()
    print('Test 1: OK')

    try:
        a2 = Archiver(archive_name, 'w')
        print('THIS SHOULD NEVER BE PRINTED')
    except:
        print('Test 2: OK')

    a3 = Archiver(archive_name, 'r')
    assert a3.size() == ARCHIVE_SIZE, 'Test 3 failed'
    print('Test 3: OK')

    for i in range(0, ARCHIVE_SIZE):
        assert a3.get(f'id_{i}') == bytes(FILE_SIZE*f'{i}', 'utf-8'), 'Test 4 failed'

    print('Test 4: OK')
    print(list(a3.keys())[0:10])

    try:
        a1 = Archiver(archive_name, 'w')
    except:
        print('Test 5: OK')

    print('All tests passed')