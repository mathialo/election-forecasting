import numpy as np
import pandas as pd

from valgsim.data_loader import electorate, load_data
from valgsim.electoral import distribute, sainte_lagues
from valgsim.simulator import simulate_election


def run_model(simulations: int) -> pd.DataFrame:
    national_poll_data = load_data("2021-08-01", "2021-09-01")

    parties = national_poll_data.columns[~national_poll_data.columns.isin(["Måling", "Dato"])]
    votes = pd.DataFrame(index=np.arange(simulations), columns=parties).fillna(0)
    representatives = pd.DataFrame(index=np.arange(simulations), columns=parties).fillna(0)

    for county in electorate:
        local_votes = simulate_election(
            electorate=electorate[county],
            local_poll_data=load_data("2021-08-01", "2021-09-01", county),
            national_poll_data=national_poll_data,
            num=simulations,
        )
        votes += local_votes
        representatives += distribute(sainte_lagues, local_votes, electorate[county].representatives)

    votes = votes.drop(columns=["Andre"])
    vote_share = votes / votes.values.sum(axis=1, keepdims=True)
    gets_leveling = vote_share >= 0.04

    print("Partiene får utjevningsmandater (sannsynlighet):")
    print(gets_leveling.mean() * 100)

    print()

    leveling = distribute(
        sainte_lagues, votes * gets_leveling, 19, given_seats=representatives.drop(columns=["Andre"])
    ).assign(Andre=0)

    reps_total = representatives + leveling
    print("Prediksjon (representanter):")
    print(reps_total.mean().astype(int))
    print()

    print("95% konfidensinterval (representanter):")
    low = (reps_total.mean() - reps_total.std()).round(1)
    high = (reps_total.mean() + reps_total.std()).round(1)
    for party in parties:
        print(f"{party:12}{low[party]} - {high[party]}")

    print()

    print("Regjeringskonstellasjoner (sannsynlighet):")
    apsp = (reps_total["Ap"] + reps_total["Sp"] >= 169 // 2 + 1).mean() * 100
    apspsv = (reps_total["Ap"] + reps_total["Sp"] + reps_total["SV"] >= 169 // 2 + 1).mean() * 100
    apspsvrmdg = (
        reps_total["Ap"] + reps_total["Sp"] + reps_total["SV"] + reps_total["Rødt"] + reps_total["MDG"] >= 169 // 2 + 1
    ).mean() * 100
    hfrp = (reps_total["Høyre"] + reps_total["Frp"] >= 169 // 2 + 1).mean() * 100
    hfrpvkrf = (
        reps_total["Høyre"] + reps_total["Frp"] + reps_total["Venstre"] + reps_total["KrF"] >= 169 // 2 + 1
    ).mean() * 100
    print(f"{'Ap+Sp':15}{apsp}")
    print(f"{'Ap+Sp+SV':15}{apspsv}")
    print(f"{'Ap+Sp+SV+R+MDG':15}{apspsvrmdg}")
    print(f"{'H+FrP':15}{hfrp}")
    print(f"{'H+FrP+V+KrF':15}{hfrpvkrf}")
