from datetime import datetime

import numpy as np
import pandas as pd

from valgsim.data_loader import assumed_participation, participation_2017


def simulate_election(
    electorate: pd.Series, local_poll_data: pd.DataFrame, national_poll_data: pd.DataFrame, num: int
) -> pd.DataFrame:
    local_df = local_poll_data.drop(columns=["Måling", "Dato"])
    national_df = national_poll_data.drop(columns=["Måling", "Dato"])

    means: pd.Series = local_df.mean().fillna(national_df.mean())
    predicted_means = predict_future(local_poll_data, national_poll_data, datetime(2021, 9, 13))

    mean_reversal = np.random.uniform()
    reversed_means = means * mean_reversal + predicted_means * (1 - mean_reversal)

    stds: pd.Series = local_df.std().fillna(national_df.std()) * 1.5

    vote_distributions = np.random.normal(reversed_means.values, stds.values, [num, reversed_means.size]).astype(
        np.float64
    )
    vote_distributions = np.clip(vote_distributions, 1, 100)
    vote_distributions = vote_distributions / vote_distributions.sum(axis=1, keepdims=True)

    participations = np.random.normal(participation_2017[electorate.name], 0.3, (num, reversed_means.size))

    votes = vote_distributions * participations * electorate["population"]

    return pd.DataFrame(votes.astype(np.int), columns=means.index)


def linear_model(poll_data: pd.DataFrame) -> np.array:
    dates = poll_data["Dato"]
    series = poll_data.drop(columns=["Måling", "Dato"])

    return np.polyfit(dates.view("uint64"), series, 1)


def predict_future(local_poll_data: pd.DataFrame, national_poll_data: pd.DataFrame, target_date: datetime) -> pd.Series:
    parties = national_poll_data.drop(columns=["Måling", "Dato"]).columns

    local_fit = linear_model(local_poll_data)
    # national_fit = linear_model(national_poll_data)

    # Use national trends
    # local_fit[:, 0] = national_fit[:, 0]

    ns_timestamp = int(target_date.timestamp() * 1e9) * np.ones(parties.size)

    return pd.DataFrame(np.expand_dims(np.polyval(local_fit, ns_timestamp), 0), columns=parties).loc[0]
