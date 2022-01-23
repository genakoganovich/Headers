from os import listdir
from os.path import isfile, join
import struct

HEADERS_FILE_PSTM = 'DS-0244_MF-PSTM_on_Topography.txt'
HEADERS_FILE_PSDM = 'DS-0244_MF-PSDM_on_datum.txt'
HEADERS_FILE_PSDM_VEL = 'DS-0244_MF-PSDM_velocity_on_datum.txt'
HEADERS_FILE_NMO_STACK = 'DS-0244_NMO_Stack_on_Topography.txt'
HEADERS_FILE_POSTSTM = 'DS-0244_PostSTM_on_Topography.txt'
HEADERS_FILE_STACKING_VELOCITY = 'DS-0244_Stacking_Velocity_on_Topography.txt'
HEADERS_FILE_GEOM_GATHERS = 'DS-0244_Geom_Gathers_on_Topography.txt'

# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/MF PSDM/psdm/West/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/West/NMO Stack/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/South/PostSTM/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/West/PostSTM/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/South/Stacking Velocity/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/West/Stacking Velocity/'
# DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/South/GeomGathers/'
DIR_PATH = 'd:/data/_FTP Incoming/Israel Projects/_Priority_Lines/_Deliverables to GII/StandardProcessing/West/GeomGathers/'


class Sgy:
    TEXT_HEADER_SIZE = 3200
    BIN_HEADER_SIZE = 400
    S_I = 17
    S_N = 21
    DATUM = 52

    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
        self.full_name = path + file_name
        self.line_name = file_name[0:str(file_name).find('__')]
        self.s_interval = Sgy.get_s_interval(self.full_name)
        self.s_number = Sgy.get_s_number(self.full_name)
        self.s_len = Sgy.get_s_len(self.full_name)
        self.datum = Sgy.get_datum(self.full_name)

    def __repr__(self):
        rep = 'Sgy(' + self.path + ', ' \
              + self.file_name + ', ' \
              + str(self.s_interval) + ', ' \
              + str(self.s_len) + ', '\
              + str(self.datum) + ')'
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

    @staticmethod
    def get_datum(file_name):
        return int(Sgy.get_value(file_name, Sgy.TEXT_HEADER_SIZE + Sgy.BIN_HEADER_SIZE + Sgy.DATUM, '>I', 4) / 100)


def replace_line(line, line_name):
    left = line[0:36].strip().replace('LINE: DS-0244', 'LINE: ' + str(line_name)).ljust(36)
    right = line[36:-1].strip()
    return (left + right).upper()


def replace_datum(line, datum):
    left = line[0:36].strip().replace('TOPOGRAPHY', str(datum) + ' M').ljust(36)
    right = line[36:-1].strip()
    return (left + right).upper()


def read_txt_header(header_file_name):
    with open(header_file_name, 'rt') as f:
        return f.readlines()


def save_txt_header_to_target(header_lines, sgy, header_type):
    with open(sgy.full_name, 'r+b') as f:
        count = 0
        for line in header_lines:
            count += 1
            if count == 2:
                line = replace_line(line, sgy.line_name)

            if count == 3 and header_type == 'TIME':
                line = line.strip().replace('2 MS', str(sgy.s_interval) + ' MS')
                line = line.strip().replace('3996 MS', str(sgy.s_len) + ' MS')

            if count == 3 and header_type == 'DEPTH':
                line = line.strip().replace('2 MS', str(sgy.s_interval) + ' M')
                line = line.strip().replace('3996 MS', str(sgy.s_len) + ' M')

            if count == 7 and header_type == 'DEPTH':
                line = replace_datum(line, sgy.datum)

            f.write(line.strip().ljust(80).encode('cp500'))


def create_file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def import_txt_header(header_lines, path, header_type):
    for target_file in create_file_list(path):
        save_txt_header_to_target(header_lines, Sgy(path, target_file), header_type)


if __name__ == '__main__':
    # import_txt_header(read_txt_header(HEADERS_FILE_TIME), DIR_PATH, 'TIME')
    # import_txt_header(read_txt_header(HEADERS_FILE_DEPTH), DIR_PATH, 'DEPTH')
    # import_txt_header(read_txt_header(HEADERS_FILE_DEPTH_VEL), DIR_PATH, 'DEPTH')
    # import_txt_header(read_txt_header(HEADERS_FILE_NMO_STACK), DIR_PATH, 'TIME')
    # import_txt_header(read_txt_header(HEADERS_FILE_POSTSTM), DIR_PATH, 'TIME')
    # import_txt_header(read_txt_header(HEADERS_FILE_STACKING_VELOCITY), DIR_PATH, 'TIME')
    import_txt_header(read_txt_header(HEADERS_FILE_GEOM_GATHERS), DIR_PATH, 'TIME')
