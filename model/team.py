from dataclasses import dataclass

@dataclass
class Team:
    id: int
    year: int
    team_code: int
    name: str

    def __str__(self):
        return f'{self.name} ({self.year})'