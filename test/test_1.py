import os
import random
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
        print('Test 3: THIS SHOULD NEVER BE PRINTED')
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

    ''' Test 6'''
    try:
        a6 = Archiver(archive_name, 'w')
        print('Test 6: THIS SHOULD NEVER BE PRINTED')
    except:
        print('Test 6: OK')

    ''' Test 7'''
    a7 = Archiver(archive_name, 'w', overwrite=True)
    assert a7.size() == 0, 'Test 7 failed'
    for i in range(0, ARCHIVE_SIZE):
        a7.add(f'id_{i}', bytes(FILE_SIZE*f'{i}', 'utf-8'))
    assert a7.size() == ARCHIVE_SIZE, 'Test 7 failed'
    a7.flush()
    print('Test 7: OK')

    ''' Test 8: Archiver remove '''
    a8 = Archiver(archive_name, 'w', overwrite=True)
    assert a8.size() == 0, 'Test 8 failed'
    for i in range(0, ARCHIVE_SIZE):
        a8.add(f'id_{i}', bytes(FILE_SIZE*f'{i}', 'utf-8'))
    assert a8.size() == len(a8.keys()) == ARCHIVE_SIZE, 'Test 8 failed'
    N_REMOVE = 5
    random_sample = random.sample(range(0, ARCHIVE_SIZE), N_REMOVE)
    assert len(random_sample) == N_REMOVE, 'Test 8 failed'
    a8_keys = a8.keys()
    keys_2_remove = [a8_keys[k] for k in random_sample]
    for k in keys_2_remove:
        a8.remove(k)
    a8_keys_left = [k for k in a8_keys if k not in keys_2_remove]
    assert a8.keys() == a8_keys_left, 'Test 8 failed'
    assert a8.size() == len(a8.keys()) == (ARCHIVE_SIZE - N_REMOVE), 'Test 8 failed'
    a8.flush()
    a8 = Archiver(archive_name, 'r')
    assert a8.keys() == a8_keys_left, 'Test 8 failed'
    print('Test 8: OK')

    print('All tests passed')