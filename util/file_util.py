import os


def delete_file(abs_file_path):
    os.remove(abs_file_path)


def write(abs_file_path, context):
    mkdir_if_not_exists(get_path(abs_file_path))
    data_file = open(abs_file_path, 'a+')
    data_file.write(context)
    data_file.flush()
    data_file.close()


def writelines(abs_file_path, context):
    mkdir_if_not_exists(get_path(abs_file_path))
    data_file = open(abs_file_path, 'a+')
    data_file.writelines(context)
    data_file.flush()
    data_file.close()


def exists(path):
    return os.path.exists(path)


def not_exists(path):
    return not exists(path)


def read_file(abs_file_path):
    with open(abs_file_path, "r") as f:
        lines = f.readlines()
        f.close()
        return lines


# 根据文件的绝对路径获取文件所在的目录
def get_path(abs_file_path):
    return os.path.dirname(os.path.abspath(abs_file_path))


def mkdir_if_not_exists(d):
    if not os.path.exists(d):
        os.makedirs(d)


def cover(abs_file_path, lines):
    delete_file(abs_file_path)
    write(abs_file_path, lines)


def get_last_line(file):
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        return f.readline().decode()


def list_all_file(path):
    from pathlib import Path
    p = Path(path)
    return [x for x in p.iterdir() if x.is_file()]


def list_all_dir(path):
    from pathlib import Path
    p = Path(path)
    return [x for x in p.iterdir() if x.is_dir()]


def get_file_name(abs_path, with_suffix=True):
    file_name = os.path.basename(abs_path)
    if not with_suffix:
        file_name = file_name.split(".")[0]
    return file_name
