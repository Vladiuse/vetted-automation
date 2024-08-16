import csv
from dataclasses import dataclass

from .config import RECRUITERS_PATH


def get_recruiters_data(file_path: str) -> list[list]:
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


@dataclass
class Recruiter:
    name: str
    is_active: bool


class RecruiterForm:

    def __init__(self, data):
        self.data = data

    def validate(self) -> None:
        self.data['name'] = RecruiterForm._validate_name(self.data['name'])
        self.data['is_active'] = RecruiterForm._validate_is_active(self.data['is_active'])

        setattr(self, 'is_checked', True)

    def create(self) -> Recruiter:
        if not hasattr(self, 'is_checked'):
            raise AttributeError('call .validate() before creating')
        return Recruiter(
            name=self.data['name'],
            is_active=self.data['is_active'],
        )

    @staticmethod
    def _validate_name(value: str) -> str:
        value = value.strip()
        return value

    @staticmethod
    def _validate_is_active(value: str) -> bool:
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

    def feed_from_raw_data(self, data: list) -> None:
        for name, is_active in data:
            form = RecruiterForm({
                'name': name,
                'is_active': is_active,
            })
            form.validate()
            recruiter = form.create()
            self.add(recruiter)

    def add(self, recruiter: Recruiter) -> None:
        self._recruiters.append(recruiter)
        self._validate()

    def _get_active(self) -> list[Recruiter]:
        active_recs = filter(lambda rec: rec.is_active, self)
        return list(active_recs)

    def get_active_rec_names(self) -> list[str]:
        if not self._get_active():
            raise ValueError('At least one recruiter must be active')
        names = [rec.name for rec in self._get_active()]
        return names

    def _validate(self) -> None:
        self._validate_all_names_unique()

    def _validate_all_names_unique(self) -> None:
        names = []
        for rec in self._recruiters:
            if rec.name not in names:
                names.append(rec.name)
            else:
                raise ValueError(f'The name {rec.name} is duplicated in file')


recruiters_data = get_recruiters_data(RECRUITERS_PATH)
recruiters = Recruiters()
recruiters.feed_from_raw_data(recruiters_data)
