import numpy as np
import pandas as pd

from valgsim.data_loader import assumed_participation, district_ids


def simulate_election(
    electorate: pd.Series, local_poll_data: pd.DataFrame, national_poll_data: pd.DataFrame, num: int
) -> pd.DataFrame:
    local_df = local_poll_data.drop(columns=["Måling", "Dato"])
    national_df = national_poll_data.drop(columns=["Måling", "Dato"])

    means: pd.Series = local_df.mean()
    stds: pd.Series = local_df.std().fillna(national_df.std()) * 2.5

    vote_distributions = np.random.normal(means.values, stds.values, [num, means.size]).astype(np.float64)
    vote_distributions = np.clip(vote_distributions, 1, 100)
    vote_distributions = vote_distributions / vote_distributions.sum(axis=1, keepdims=True)

    votes = vote_distributions * assumed_participation * electorate["population"]

    return pd.DataFrame(votes.astype(np.int), columns=means.index)
