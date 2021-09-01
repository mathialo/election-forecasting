import re
from io import StringIO

import pandas as pd
import requests

district_ids = pd.DataFrame(
    {
        "Akershus": 2,
        "Aust-Agder": 9,
        "Buskerud": 6,
        "Finnmark": 20,
        "Hedmark": 4,
        "Hordaland": 12,
        "Møre og Romsdal": 15,
        "Nord-Trøndelag": 17,
        "Nordland": 18,
        "Oppland": 5,
        "Oslo": 3,
        "Rogaland": 11,
        "Sogn og Fjordane": 14,
        "Sør-Trøndelag": 16,
        "Telemark": 8,
        "Troms": 19,
        "Vest-Agder": 10,
        "Vestfold": 7,
        "Østfold": 1,
    },
    index=["id"],
)

representatives = pd.DataFrame(
    {
        "Akershus": 18,
        "Aust-Agder": 3,
        "Buskerud": 7,
        "Finnmark": 4,
        "Hedmark": 6,
        "Hordaland": 15,
        "Møre og Romsdal": 7,
        "Nord-Trøndelag": 4,
        "Nordland": 8,
        "Oppland": 5,
        "Oslo": 19,
        "Rogaland": 13,
        "Sogn og Fjordane": 3,
        "Sør-Trøndelag": 9,
        "Telemark": 5,
        "Troms": 5,
        "Vest-Agder": 5,
        "Vestfold": 6,
        "Østfold": 8,
    },
    index=["representatives"],
    dtype=int,
)

population = pd.DataFrame(
    {
        "Østfold": 222500,
        "Akershus": 467100,
        "Oslo": 483300,
        "Hedmark": 151600,
        "Oppland": 132400,
        "Buskerud": 191100,
        "Vestfold": 182000,
        "Telemark": 130700,
        "Aust-Agder": 86700,
        "Vest-Agder": 137200,
        "Rogaland": 331800,
        "Hordaland": 381600,
        "Sogn og Fjordane": 78300,
        "Møre og Romsdal": 191900,
        "Sør-Trøndelag": 246900,
        "Nord-Trøndelag": 100500,
        "Nordland": 181600,
        "Troms": 124500,
        "Finnmark": 54500,
    },
    index=["population"],
)


participation_2017 = pd.DataFrame(
    {
        "Østfold": 0.750,
        "Akershus": 0.812,
        "Oslo": 0.802,
        "Hedmark": 0.767,
        "Oppland": 0.762,
        "Buskerud": 0.773,
        "Vestfold": 0.776,
        "Telemark": 0.752,
        "Aust-Agder": 0.771,
        "Vest-Agder": 0.770,
        "Rogaland": 0.786,
        "Hordaland": 0.811,
        "Sogn og Fjordane": 0.794,
        "Møre og Romsdal": 0.774,
        "Sør-Trøndelag": 0.788,
        "Nord-Trøndelag": 0.773,
        "Nordland": 0.751,
        "Troms": 0.756,
        "Finnmark": 0.726,
    },
    index=["participation"],
)


electorate = pd.concat([district_ids, population, representatives])


assumed_participation = 0.75


def load_data(from_date: str, to_date: str, district="Alle", remote_load=True) -> pd.DataFrame:
    if remote_load:
        response = requests.get(
            f"http://www.pollofpolls.no/lastned.csv?type=riks&kommuneid={0 if district == 'Alle' else district_ids.get(district).id}&tabell=liste_galluper&start={from_date}&slutt={to_date}"
        )

        csv = response.content.decode(encoding="latin_1")
        csv = "\n".join([l for l in csv.split("\n")[2:]])
        csv = re.sub(r"\s*\(\d+\)", "", csv)
        csv = re.sub(r",", ".", csv)

        data: pd.DataFrame = pd.read_csv(StringIO(csv), delimiter=";")
        data["Dato"] = pd.to_datetime(data["Dato"], dayfirst=True)
        with open(f"data/{district}.csv", "w") as f:
            data.to_csv(f, index=False)
        return data

    else:
        data = pd.read_csv(f"data/{district}.csv")
        data["Dato"] = pd.to_datetime(data["Dato"])
        return data
