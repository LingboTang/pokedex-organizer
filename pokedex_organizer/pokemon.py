import csv
from dataclasses import dataclass, field


CSV_COLUMNS = [
    "Pokemon Name", "CP", "Attack", "Defense", "HP",
    "Shiny", "Lucky", "Dynamax", "Move Set",
]


def _parse_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes")


@dataclass
class Pokemon:
    name: str
    cp: int
    attack: int  # Attack IV (0-15)
    defense: int  # Defense IV (0-15)
    hp: int  # Stamina IV (0-15)
    shiny: bool
    lucky: bool
    dynamax: bool
    move_set: str
    dps: float = field(default=0.0)
    decision: str = field(default="")

    @property
    def iv_sum(self):
        return self.attack + self.defense + self.hp

    @classmethod
    def from_row(cls, row):
        return cls(
            name=row["Pokemon Name"].strip(),
            cp=int(row["CP"]),
            attack=int(row["Attack"]),
            defense=int(row["Defense"]),
            hp=int(row["HP"]),
            shiny=_parse_bool(row["Shiny"]),
            lucky=_parse_bool(row["Lucky"]),
            dynamax=_parse_bool(row["Dynamax"]),
            move_set=row["Move Set"].strip(),
        )

    def to_row(self):
        return {
            "Pokemon Name": self.name,
            "CP": self.cp,
            "Attack": self.attack,
            "Defense": self.defense,
            "HP": self.hp,
            "Shiny": self.shiny,
            "Lucky": self.lucky,
            "Dynamax": self.dynamax,
            "Move Set": self.move_set,
            "Decision": self.decision,
        }


def load_pokemon_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Pokemon.from_row(row) for row in reader]


def save_pokemon_csv(path, pokemons):
    fieldnames = CSV_COLUMNS + ["Decision"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in pokemons:
            writer.writerow(p.to_row())
