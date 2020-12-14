import sqlite3
import requests
import json


def create():
    with open("inputs.json") as f:
        inputs = json.load(f)

    headers = headers = {"Authorization": inputs["token"]}
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    try:
        c.execute("DROP TABLE email_table")
        c.execute("DROP TABLE venue_table")
        conn.commit()
    except:
        pass

    c.execute("CREATE TABLE email_table (id INTEGER, email TEXT)")
    c.execute("CREATE TABLE venue_table (id INTEGER, name TEXT)")
    conn.commit()

    # insert venues
    url_venues = f'{inputs["tabbyurl"]}/api/v1/tournaments/{inputs["tournament"]}/venues'
    venue_list = requests.get(url_venues, headers=headers).json()
    venue = ()
    venues = []
    for x in venue_list:
        venue = (x["id"], x["name"])
        venues.append(venue)

    sql = "INSERT INTO venue_table (id, name) VALUES (?, ?)"

    c.executemany(sql, venues)
    conn.commit()
    print(c.rowcount, " venues was inserted.")

    # insert speakers
    url_teams = f'{inputs["tabbyurl"]}/api/v1/tournaments/{inputs["tournament"]}/teams'
    teams = requests.get(url_teams, headers=headers).json()
    speakers = []
    speaker = ()
    for team in teams:
        for speaker_info in team["speakers"]:
            if speaker_info["email"] is not None:
                if len(speaker_info["email"]) > 1:
                    speaker = (team["id"], speaker_info["email"])
                    print(speaker)
                    speakers.append(speaker)

    sql = "INSERT INTO email_table (id, email) VALUES (?,?)"

    c.executemany(sql, speakers)
    conn.commit()
    print(c.rowcount, " speakers was inserted.")

    # insert adjudicators
    adjudicators = []
    adjudicator = ()

    url_adjudicators = f'{inputs["tabbyurl"]}/api/v1/tournaments/{inputs["tournament"]}/adjudicators'
    adjudicator_info = requests.get(url_adjudicators, headers=headers).json()

    for adj in adjudicator_info:
        if adj["email"] is not None:
            if len(adj["email"]) > 1:
                adjudicator = (adj["id"], adj["email"])
                print(adjudicator)
                adjudicators.append(adjudicator)

    sql = "INSERT INTO email_table (id, email) VALUES (?,?)"
    c.executemany(sql, adjudicators)
    conn.commit()
    print(c.rowcount, " juries was inserted.")

    conn.close()


def user_input(tabbyurl, tournament, token, room_per_zoom):

    inputs = {
        "tabbyurl": tabbyurl,
        "tournament": tournament,
        "token": token,
        "room_per_zoom": room_per_zoom,
    }

    with open("inputs.json", "w") as f:
        json.dump(inputs, f)


if __name__ == "__main__":
    create()
