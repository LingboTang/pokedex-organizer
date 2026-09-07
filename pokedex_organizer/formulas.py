"""
Official-game formulas for Combat Power (CP) and move-set DPS.

Reference data below (CPM table, base stats, move stats) is a small
illustrative subset sourced from public references (Pokemon GO Hub's CPM
table, Dittobase's move database). For production accuracy, swap
BASE_STATS / EVOLUTIONS / MOVE_DATA for the full official Niantic
GAME_MASTER dataset.
"""

import math

# CP multiplier per trainer level (official values, levels 1-40).
CPM_TABLE = {
    1: 0.094, 1.5: 0.1351374318, 2: 0.16639787, 2.5: 0.192650919,
    3: 0.21573247, 3.5: 0.2365726613, 4: 0.25572005, 4.5: 0.2735303812,
    5: 0.29024988, 5.5: 0.3060573775, 6: 0.3210876, 6.5: 0.3354450362,
    7: 0.34921268, 7.5: 0.3624577511, 8: 0.3752356, 8.5: 0.387592416,
    9: 0.39956728, 9.5: 0.4111935514, 10: 0.4225, 10.5: 0.4329264091,
    11: 0.44310755, 11.5: 0.4530599591, 12: 0.4627984, 12.5: 0.472336093,
    13: 0.48168495, 13.5: 0.4908558003, 14: 0.49985844, 14.5: 0.508701765,
    15: 0.51739395, 15.5: 0.5259425113, 16: 0.5343543, 16.5: 0.5426357375,
    17: 0.5507927, 17.5: 0.5588305862, 18: 0.5667545, 18.5: 0.5745691333,
    19: 0.5822789, 19.5: 0.5898879072, 20: 0.5974, 20.5: 0.6048236651,
    21: 0.6121573, 21.5: 0.6194041216, 22: 0.6265671, 22.5: 0.6336491432,
    23: 0.64065295, 23.5: 0.6475809666, 24: 0.65443563, 24.5: 0.6612192524,
    25: 0.667934, 25.5: 0.6745818959, 26: 0.6811649, 26.5: 0.6876849038,
    27: 0.69414365, 27.5: 0.70054287, 28: 0.7068842, 28.5: 0.7131691091,
    29: 0.7193991, 29.5: 0.7255756136, 30: 0.7317, 30.5: 0.7347410093,
    31: 0.7377695, 31.5: 0.7407855938, 32: 0.74378943, 32.5: 0.7467812109,
    33: 0.74976104, 33.5: 0.7527290867, 34: 0.7556855, 34.5: 0.7586303683,
    35: 0.76156384, 35.5: 0.7644860647, 36: 0.76739717, 36.5: 0.7702972656,
    37: 0.7731865, 37.5: 0.7760649616, 38: 0.77893275, 38.5: 0.7817900548,
    39: 0.784637, 39.5: 0.7874736075, 40: 0.7903,
}

# Sample base stats (Attack, Defense, Stamina) for a handful of species.
BASE_STATS = {
    "Bulbasaur": (118, 111, 128),
    "Ivysaur": (151, 143, 155),
    "Venusaur": (198, 189, 190),
    "Charmander": (116, 93, 118),
    "Charmeleon": (158, 126, 151),
    "Charizard": (223, 176, 186),
    "Squirtle": (94, 121, 127),
    "Wartortle": (126, 155, 158),
    "Blastoise": (171, 210, 188),
    "Pidgey": (85, 73, 111),
    "Pidgeotto": (117, 105, 143),
    "Pidgeot": (166, 154, 195),
    "Magikarp": (29, 85, 65),
    "Gyarados": (237, 197, 216),
}

# Species -> next evolution stage (sample subset).
EVOLUTIONS = {
    "Bulbasaur": "Ivysaur",
    "Ivysaur": "Venusaur",
    "Charmander": "Charmeleon",
    "Charmeleon": "Charizard",
    "Squirtle": "Wartortle",
    "Wartortle": "Blastoise",
    "Pidgey": "Pidgeotto",
    "Pidgeotto": "Pidgeot",
    "Magikarp": "Gyarados",
}

# Sample fast/charge move data: power, duration (seconds), energy.
# Fast move "energy" is energy gained per use; charge move "energy" is the
# energy cost (consumed) per use.
MOVE_DATA = {
    "fast": {
        "Tackle": {"power": 5, "duration": 0.5, "energy": 5},
        "Mud Shot": {"power": 4, "duration": 0.5, "energy": 6},
        "Shadow Claw": {"power": 6, "duration": 0.5, "energy": 4},
        "Dragon Breath": {"power": 6, "duration": 0.5, "energy": 4},
        "Ember": {"power": 10, "duration": 1.0, "energy": 10},
        "Confusion": {"power": 19, "duration": 1.5, "energy": 14},
        "Poison Jab": {"power": 13, "duration": 1.0, "energy": 9},
        "Counter": {"power": 13, "duration": 1.0, "energy": 9},
        "Fire Fang": {"power": 13, "duration": 1.0, "energy": 9},
        "Vine Whip": {"power": 7, "duration": 0.6, "energy": 6},
        "Water Gun": {"power": 6, "duration": 0.6, "energy": 6},
        "Wing Attack": {"power": 8, "duration": 0.6, "energy": 6},
    },
    "charge": {
        "Frenzy Plant": {"power": 100, "duration": 2.5, "energy": 50},
        "Hydro Cannon": {"power": 90, "duration": 2.0, "energy": 50},
        "Blast Burn": {"power": 120, "duration": 3.5, "energy": 50},
        "Solar Beam": {"power": 180, "duration": 5.0, "energy": 100},
        "Close Combat": {"power": 105, "duration": 2.5, "energy": 100},
        "Dragon Claw": {"power": 45, "duration": 1.5, "energy": 33},
        "Sludge Bomb": {"power": 85, "duration": 2.5, "energy": 50},
        "Stone Edge": {"power": 105, "duration": 2.5, "energy": 100},
        "Earthquake": {"power": 140, "duration": 3.5, "energy": 100},
        "Focus Blast": {"power": 140, "duration": 3.5, "energy": 100},
        "Body Slam": {"power": 50, "duration": 2.0, "energy": 33},
        "Hyper Beam": {"power": 150, "duration": 4.0, "energy": 100},
        "Twister": {"power": 45, "duration": 1.9, "energy": 33},
        "Aqua Tail": {"power": 50, "duration": 1.9, "energy": 33},
    },
}


def calculate_cp(base_attack, base_defense, base_stamina,
                  iv_attack, iv_defense, iv_stamina, level):
    """Official CP formula: floor((Atk * sqrt(Def) * sqrt(Sta) * CPM^2) / 10), min 10."""
    cpm = CPM_TABLE.get(level)
    if cpm is None:
        raise ValueError(f"Unknown trainer level: {level}")

    attack = base_attack + iv_attack
    defense = base_defense + iv_defense
    stamina = base_stamina + iv_stamina

    cp = math.floor((attack * math.sqrt(defense) * math.sqrt(stamina) * cpm ** 2) / 10)
    return max(cp, 10)


def calculate_evolution_cp(pokemon_name, iv_attack, iv_defense, iv_stamina, level):
    """
    CP the Pokémon would have after evolving, assuming the same IVs and level
    (evolving does not change IVs or trainer-relative level).
    Returns None if the species is unknown or has no further evolution.
    """
    evolved_name = EVOLUTIONS.get(pokemon_name)
    if evolved_name is None:
        return None

    base_stats = BASE_STATS.get(evolved_name)
    if base_stats is None:
        return None

    base_attack, base_defense, base_stamina = base_stats
    return calculate_cp(base_attack, base_defense, base_stamina,
                         iv_attack, iv_defense, iv_stamina, level)


def parse_moveset(move_set):
    """Parse a "FastMove/ChargeMove" string from the CSV's Move Set column."""
    fast_name, _, charge_name = move_set.partition("/")
    return fast_name.strip(), charge_name.strip()


def calculate_moveset_dps(fast_move_name, charge_move_name):
    """
    DPS for a fast+charge moveset using the standard energy-cycle formula:
    figure out how many fast moves are needed to generate enough energy for
    one charge move, then DPS = total cycle damage / total cycle time.
    Returns 0.0 if either move is not recognized.
    """
    fast = MOVE_DATA["fast"].get(fast_move_name)
    charge = MOVE_DATA["charge"].get(charge_move_name)
    if fast is None or charge is None:
        return 0.0

    fast_moves_needed = math.ceil(charge["energy"] / fast["energy"])
    cycle_damage = fast_moves_needed * fast["power"] + charge["power"]
    cycle_duration = fast_moves_needed * fast["duration"] + charge["duration"]

    return cycle_damage / cycle_duration


def calculate_dps_from_moveset_string(move_set):
    """Convenience wrapper: parse a "Fast/Charge" string and compute its DPS."""
    fast_name, charge_name = parse_moveset(move_set)
    return calculate_moveset_dps(fast_name, charge_name)
