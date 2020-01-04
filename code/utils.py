import random


def seed_random(seed: int, use_fixed: bool) -> int:
    if not use_fixed:
        import sys  # noqa

        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed
