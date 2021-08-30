from typing import Callable, Optional

import numpy as np
import pandas as pd


def distribute(
    method: Callable[[np.array, int, np.array], np.array],
    votes: pd.DataFrame,
    seats: int,
    given_seats: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    vote_data = votes.values.astype(np.float64)
    given_seats = np.zeros_like(vote_data) if given_seats is None else given_seats.values
    return pd.DataFrame(method(vote_data, seats, given_seats), columns=votes.columns)


def sainte_lagues(votes: np.array, seats: int, given_seats: np.array = None, first_divisor=1.4) -> np.array:
    new_seats = np.zeros_like(given_seats)

    for seat in range(seats):
        total_seats = given_seats + new_seats
        has_seats = total_seats != 0
        round = votes * has_seats / (total_seats * 2 + 1) + votes * ~has_seats / first_divisor
        winner = np.argmax(round, axis=1)
        new_seats[np.arange(round.shape[0]), winner] += 1

    return new_seats.astype(np.int)
