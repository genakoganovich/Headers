from os import listdir
from os.path import isfile, join
import struct

headers_file = 'headers.txt'
dir_path = 'c:/data/input/'


def replace_line(line, line_name):
    left = line[0:36].strip().replace('LINE: DS-0244', 'LINE: ' + str(line_name)).ljust(36)
    right = line[36:-1].strip()
    return left + right


def read_txt_header(header_file_name):
    with open(header_file_name, 'rt') as f:
        return f.readlines()


def save_txt_header_to_target(header_lines, target_path, target_file):
    full_name = target_path + target_file
    with open(full_name, 'r+b') as f:
        count = 0
        for line in header_lines:
            count += 1
            if count == 2:
                line = replace_line(line, get_line_name(target_file))

            if count == 3:
                line = line.strip().replace('2 MS', str(get_s_interval(full_name)) + ' MS')
                line = line.strip().replace('3996 MS', str(get_s_len(full_name)) + ' MS')

            f.write(line.strip().ljust(80).encode('cp850'))


def get_line_name(file_name):
    return file_name[0:str(file_name).find('__')]


def get_value(file_name, position, format_character, size):
    with open(file_name, 'rb') as f:
        f.seek(position)
        return int(struct.unpack(format_character, f.read(size))[0])


def get_s_interval(file_name):
    return int(get_value(file_name, 3200 + 17, 'h', 2) / 1000)


def get_s_number(file_name):
    return get_value(file_name, 3200 + 21, 'h', 2)


def get_s_len(file_name):
    return get_s_interval(file_name) * (get_s_number(file_name) - 1)


def create_file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def import_txt_header(header_lines, path):
    for target_file in create_file_list(path):
        save_txt_header_to_target(header_lines, path, target_file)


if __name__ == '__main__':
    import_txt_header(read_txt_header(headers_file), dir_path)
