import argparse
import os

from .decision import decide
from .enums import UserBehavior
from .formulas import calculate_dps_from_moveset_string
from .pokemon import load_pokemon_csv, save_pokemon_csv


def _default_output_path(input_path):
    base, ext = os.path.splitext(input_path)
    return f"{base}_decisions{ext or '.csv'}"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pokedex-organizer",
        description="Decide which Pokemon to KEEP or TRANSFER based on your play style.",
    )
    parser.add_argument("input_csv", help="Path to the input CSV of Pokemon base stats.")
    parser.add_argument(
        "behavior",
        choices=[b.value for b in UserBehavior],
        help="How you mainly play: RAID, COLLECTION, GYM, or CASUAL.",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Path to the output CSV (default: <input>_decisions.csv).",
    )
    parser.add_argument(
        "--keep-top",
        type=int,
        default=1,
        help="Number of top Pokemon per species to KEEP (default: 1).",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    behavior = UserBehavior(args.behavior)

    pokemons = load_pokemon_csv(args.input_csv)
    for pokemon in pokemons:
        pokemon.dps = calculate_dps_from_moveset_string(pokemon.move_set)

    decide(pokemons, behavior, keep_top_n=args.keep_top)

    output_path = args.output or _default_output_path(args.input_csv)
    save_pokemon_csv(output_path, pokemons)
    print(f"Wrote {len(pokemons)} Pokemon decisions to {output_path}")


if __name__ == "__main__":
    main()
