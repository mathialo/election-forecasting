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

    votes_core = votes.drop(columns=["Andre"])
    vote_share_core = votes_core / votes_core.values.sum(axis=1, keepdims=True)
    gets_leveling = vote_share_core >= 0.04

    print("Partiene får utjevningsmandater (sannsynlighet):")
    print(gets_leveling.mean() * 100)

    print()

    leveling = distribute(
        sainte_lagues, votes_core * gets_leveling, 19, given_seats=representatives.drop(columns=["Andre"])
    ).assign(Andre=0)

    print("Prediksjon (nasjonal oppslutning):")
    vote_share = votes / votes.values.sum(axis=1, keepdims=True)
    print(vote_share.mean().multiply(100).round(1))
    print()

    print("Persentiler (nasjonal oppslutning):")
    vote_p1 = vote_share.quantile(q=0.01).multiply(100).round(1)
    vote_p5 = vote_share.quantile(q=0.05).multiply(100).round(1)
    vote_p10 = vote_share.quantile(q=0.1).multiply(100).round(1)
    vote_p25 = vote_share.quantile(q=0.25).multiply(100).round(1)
    vote_p50 = vote_share.quantile(q=0.5).multiply(100).round(1)
    vote_p75 = vote_share.quantile(q=0.75).multiply(100).round(1)
    vote_p90 = vote_share.quantile(q=0.90).multiply(100).round(1)
    vote_p95 = vote_share.quantile(q=0.95).multiply(100).round(1)
    vote_p99 = vote_share.quantile(q=0.99).multiply(100).round(1)
    print(f"{'':12}{'1%':<6}{'5%':<6}{'10%':<6}{'25%':<6}{'50%':<6}{'75%':<6}{'90%':<6}{'95%':<6}{'99%':<6}")
    for party in parties:
        print(
            f"{party:12}{vote_p1[party]:<6}{vote_p5[party]:<6}{vote_p10[party]:<6}{vote_p25[party]:<6}{vote_p50[party]:<6}{vote_p75[party]:<6}{vote_p90[party]:<6}{vote_p95[party]:<6}{vote_p99[party]:<6}"
        )

    print()

    reps_total: pd.DataFrame = representatives + leveling
    print("Prediksjon (representanter):")
    print(reps_total.mean().astype(int))
    print()

    print("Persentiler (representanter):")
    seats_p1 = reps_total.quantile(q=0.01).astype(int)
    seats_p5 = reps_total.quantile(q=0.05).astype(int)
    seats_p10 = reps_total.quantile(q=0.1).astype(int)
    seats_p25 = reps_total.quantile(q=0.25).astype(int)
    seats_p50 = reps_total.quantile(q=0.5).astype(int)
    seats_p75 = reps_total.quantile(q=0.75).astype(int)
    seats_p90 = reps_total.quantile(q=0.90).astype(int)
    seats_p95 = reps_total.quantile(q=0.95).astype(int)
    seats_p99 = reps_total.quantile(q=0.99).astype(int)
    print(f"{'':12}{'1%':<6}{'5%':<6}{'10%':<6}{'25%':<6}{'50%':<6}{'75%':<6}{'90%':<6}{'95%':<6}{'99%':<6}")
    for party in parties:
        print(
            f"{party:12}{seats_p1[party]:<6}{seats_p5[party]:<6}{seats_p10[party]:<6}{seats_p25[party]:<6}{seats_p50[party]:<6}{seats_p75[party]:<6}{seats_p90[party]:<6}{seats_p95[party]:<6}{seats_p99[party]:<6}"
        )

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
    print(f"{'Ap+Sp':15}{apsp.round(2)}")
    print(f"{'Ap+Sp+SV':15}{apspsv.round(2)}")
    print(f"{'Ap+Sp+SV+R+MDG':15}{apspsvrmdg.round(2)}")
    print(f"{'H+FrP':15}{hfrp.round(2)}")
    print(f"{'H+FrP+V+KrF':15}{hfrpvkrf.round(2)}")
