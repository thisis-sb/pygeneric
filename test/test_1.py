import os
from archiver import Archiver

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    LOG_DIR = os.path.join(os.getenv('HOME_DIR'), '98_log/pygeneric')
    archive_name = LOG_DIR + '/test_archive.zip'
    ARCHIVE_SIZE = int(1000)
    FILE_SIZE    = 10000

    ''' Test 1'''
    if os.path.exists(archive_name):
        os.remove(archive_name)
    a1 = Archiver(archive_name, 'w')
    for i in range(0, ARCHIVE_SIZE):
        a1.add(f'id_{i}', bytes(FILE_SIZE*f'{i}', 'utf-8'))
    a1.flush()
    print('Test 1: OK')

    ''' Test 2'''
    a2 = Archiver(archive_name, mode='w', update=True)
    assert a2.size() == ARCHIVE_SIZE, f'Test 2 failed'
    for i in range(ARCHIVE_SIZE, 2*ARCHIVE_SIZE):
        a2.add(f'id_{i}', bytes(FILE_SIZE * f'{i}', 'utf-8'))
    assert a2.size() == (2 * ARCHIVE_SIZE), 'Test 2 failed'
    a2.flush()
    a2 = Archiver(archive_name, 'r')
    assert a2.size() == (2 * ARCHIVE_SIZE), 'Test 2 failed'
    print('Test 2: OK')

    ''' Test 3'''
    try:
        a3 = Archiver(archive_name, 'w')
        print('THIS SHOULD NEVER BE PRINTED')
    except:
        print('Test 3: OK')

    ''' Test 4'''
    a4 = Archiver(archive_name, 'r')
    assert a4.size() == (2 * ARCHIVE_SIZE), 'Test 4 failed'
    for i in range(0, (2 * ARCHIVE_SIZE)):
        assert a4.get(f'id_{i}') == bytes(FILE_SIZE*f'{i}', 'utf-8'), 'Test 4 failed'
    print('Test 4: OK')
    print(list(a4.keys())[0:10])

    ''' Test 5'''
    try:
        a5 = Archiver(archive_name, 'w')
    except:
        print('Test 5: OK')

    print('All tests passed')