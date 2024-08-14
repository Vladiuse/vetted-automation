import csv


def get_recruiters_data(file_path: str) -> list:
    recruiters_data = list()
    with open(file_path, encoding='utf-8', ) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                name, is_active = row
            except ValueError:
                raise ValueError(f'Incorrect items count in row, must be 2, actual {len(row)}')
            recruiters_data.append([name, is_active])
    return recruiters_data


class Recruiter:

    def __init__(self, name: str, is_active: bool):
        self.name = name
        self.is_active = is_active


class RecruiterForm:

    def __init__(self, data):
        self.data = data

    def validate(self):
        self.data['name'] = RecruiterForm._validate_name(self.data['name'])
        self.data['is_active'] = RecruiterForm._validate_is_active(self.data['is_active'])

        setattr(self, 'is_checked', True)

    def create(self):
        if not hasattr(self, 'is_checked'):
            raise AttributeError('call .validate() before creating')
        return Recruiter(
            name=self.data['name'],
            is_active=self.data['is_active'],
        )

    @staticmethod
    def _validate_name(value):
        value = value.strip()
        return value

    @staticmethod
    def _validate_is_active(value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f'is_valid param must be integer, not "{value}"')
        if value not in [0, 1]:
            raise ValueError(f'is_valid param must be 0 or 1, not {value}')
        value = bool(value)
        return value


class Recruiters:
    def __init__(self):
        self._recruiters = list()
        self.i = 0

    def __iter__(self):
        return iter(self._recruiters)

    def __len__(self):
        return len(self._recruiters)

    def feed_from_raw_data(self, data: list):
        for name, is_active in data:
            form = RecruiterForm({
                'name': name,
                'is_active': is_active,
            })
            form.validate()
            recruiter = form.create()
            self.add(recruiter)

    def add(self, recruiter: Recruiter):
        self._recruiters.append(recruiter)
        self._validate()

    def get_active_rec_names(self) -> list[str]:
        active_recs = filter(lambda rec: rec.is_active, self)
        names = [rec.name for rec in active_recs]
        return names

    def _validate(self):
        self._validate_all_names_unique()

    def _validate_all_names_unique(self):
        names = []
        for rec in self._recruiters:
            if rec.name not in names:
                names.append(rec.name)
            else:
                raise ValueError(f'The name {rec.name} is duplicated in file')


RECRUITERS_FILE_PATH = '../recruiters.csv'
recruiters_data = get_recruiters_data(RECRUITERS_FILE_PATH)
recruiters = Recruiters()
recruiters.feed_from_raw_data(recruiters_data)

if __name__ == '__main__':
    for rec in recruiters:
        print(rec.name, rec.is_active)
    print(recruiters.get_active_rec_names())
