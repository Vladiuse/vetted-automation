import csv

recruiters = [
    'Aaron Barton',
    'Alex Adeli',
    'Barry Heath',
    'Brian Weller',
    'Christal Hurrington',
    'Jamar Pharr',
    'James Ireland',
    'Jessica Burg',
    'Karen Freedman',
    'Kathryn Lamastra',
    'Mark Herschberg',
    'Matt Hertsenberg',
    'Megan Marshall',
    'Nick McGill',
    'Peter Nooteboom',
    'Shardai Johnson',
    'Sydney Buckner',
]


def get_recruiters_data(file_path: str) -> list:
    recruiters_data = list()
    with open(file_path, encoding='utf-8', ) as file:
        reader = csv.reader(file)
        next(reader)
        for name, is_active in reader:
            name = name.strip()
            try:
                is_active = bool(is_active)
                if is_active not in [0, 1]:
                    raise ValueError
            except ValueError:
                raise ValueError('is_active param must be 0 or 1')
            else:
                recruiters_data.append([name, is_active])
    return recruiters_data


class Recruiter:

    def __init__(self, name: str, is_active: bool):
        self.name = name
        self.is_active = is_active


class Recruiters:
    def __init__(self, recruiters: list[Recruiter]):
        self.recruiters = recruiters


recruiters_data = get_recruiters_data('../../recruiters.csv')
recruiters = []
for name, is_active in recruiters_data:
    recruiters.append(Recruiter(name, is_active))

if __name__ == '__main__':
    get_recruiters_data('../../recruiters.csv')
