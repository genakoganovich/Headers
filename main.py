from os import listdir
from os.path import isfile, join
import struct

HEADERS_FILE = 'headers.txt'
DIR_PATH = 'd:/data/Depth/gSpace/004_pstm/add_pstm_save/'


class Sgy:
    TEXT_HEADER_SIZE = 3200
    S_I = 17
    S_N = 21

    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
        self.full_name = path + file_name
        self.line_name = file_name[0:str(file_name).find('__')]
        self.s_interval = Sgy.get_s_interval(self.full_name)
        self.s_number = Sgy.get_s_number(self.full_name)
        self.s_len = Sgy.get_s_len(self.full_name)

    def __repr__(self):
        rep = 'Sgy(' + self.path + ', ' \
              + self.file_name + ', ' \
              + str(self.s_interval) + ', ' \
              + str(self.s_len) + ')'
        return rep

    @staticmethod
    def get_value(file_name, position, format_character, size):
        with open(file_name, 'rb') as f:
            f.seek(position)
            return int(struct.unpack(format_character, f.read(size))[0])

    @staticmethod
    def get_s_interval(file_name):
        return int(Sgy.get_value(file_name, Sgy.TEXT_HEADER_SIZE + Sgy.S_I, 'h', 2) / 1000)

    @staticmethod
    def get_s_number(file_name):
        return Sgy.get_value(file_name, Sgy.TEXT_HEADER_SIZE + Sgy.S_N, 'h', 2)

    @staticmethod
    def get_s_len(file_name):
        return Sgy.get_s_interval(file_name) * (Sgy.get_s_number(file_name) - 1)


def replace_line(line, line_name):
    left = line[0:36].strip().replace('LINE: DS-0244', 'LINE: ' + str(line_name)).ljust(36)
    right = line[36:-1].strip()
    return (left + right).upper()


def read_txt_header(header_file_name):
    with open(header_file_name, 'rt') as f:
        return f.readlines()


def save_txt_header_to_target(header_lines, sgy):
    with open(sgy.full_name, 'r+b') as f:
        count = 0
        for line in header_lines:
            count += 1
            if count == 2:
                line = replace_line(line, sgy.line_name)

            if count == 3:
                line = line.strip().replace('2 MS', str(sgy.s_interval) + ' MS')
                line = line.strip().replace('3996 MS', str(sgy.s_len) + ' MS')

            f.write(line.strip().ljust(80).encode('cp500'))


def create_file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def import_txt_header(header_lines, path):
    for target_file in create_file_list(path):
        save_txt_header_to_target(header_lines, Sgy(path, target_file))


if __name__ == '__main__':
    import_txt_header(read_txt_header(HEADERS_FILE), DIR_PATH)
