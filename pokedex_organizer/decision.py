import heapq
from collections import defaultdict
from itertools import count

from .enums import UserBehavior


def priority_key(pokemon, behavior):
    """
    Sort key used to rank Pokémon within a species, highest-value-first,
    tailored to how the trainer plays:
      - RAID: overall CP, then IV, then move-set DPS.
      - GYM: bulk first (Defense, then HP) since gym defenders need to stall.
      - COLLECTION / CASUAL: just total IV (Attack + Defense + HP).
    """
    if behavior == UserBehavior.RAID:
        return (pokemon.cp, pokemon.iv_sum, pokemon.dps)
    if behavior == UserBehavior.GYM:
        return (pokemon.defense, pokemon.hp)
    if behavior in (UserBehavior.COLLECTION, UserBehavior.CASUAL):
        return (pokemon.iv_sum,)
    raise ValueError(f"Unknown user behavior: {behavior}")


def rank_pokemon(pokemons, behavior):
    """Rank Pokémon best-first using a behavior-specific max-priority queue."""
    tie_breaker = count()
    heap = []
    for pokemon in pokemons:
        key = priority_key(pokemon, behavior)
        negated_key = tuple(-value for value in key)
        heapq.heappush(heap, (negated_key, next(tie_breaker), pokemon))

    ranked = []
    while heap:
        _, _, pokemon = heapq.heappop(heap)
        ranked.append(pokemon)
    return ranked


def decide(pokemons, behavior, keep_top_n=1):
    """
    Group Pokémon by species, rank each group with a behavior-specific
    priority queue, and mark the top `keep_top_n` per species as KEEP and
    the rest as TRANSFER. Shiny or Lucky Pokémon are always kept, since
    they're irreplaceable.
    """
    groups = defaultdict(list)
    for pokemon in pokemons:
        groups[pokemon.name].append(pokemon)

    for group in groups.values():
        ranked = rank_pokemon(group, behavior)
        for index, pokemon in enumerate(ranked):
            if pokemon.shiny or pokemon.lucky or index < keep_top_n:
                pokemon.decision = "KEEP"
            else:
                pokemon.decision = "TRANSFER"
