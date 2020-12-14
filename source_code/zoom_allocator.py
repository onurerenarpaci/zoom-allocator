import requests
import os
import json
import csv
import math
import sqlite3

round_number = 1


def allocate():
    with open("inputs.json") as f:
        inputs = json.load(f)

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    headers = {"Authorization": inputs["token"]}

    url_pairings = f'{inputs["tabbyurl"]}/api/v1/tournaments/{inputs["tournament"]}/rounds/{round_number}/pairings'

    pairings = requests.get(url_pairings, headers=headers).json()

    rooms = {}

    for room in pairings:
        room_id = int(room["venue"].split("/")[-1])
        c.execute(f"SELECT name FROM venue_table WHERE id = {room_id}")
        room_name = c.fetchall()[0][0]

        email_list = []

        for team in room["teams"]:
            team_id = team["team"].split("/")[-1]
            c.execute(f"SELECT email FROM email_table WHERE id = {team_id}")
            res = c.fetchall()
            email_list.append(res[0][0])
            email_list.append(res[1][0])

        chair_id = room["adjudicators"]["chair"].split("/")[-1]
        c.execute(f"SELECT email FROM email_table WHERE id = {chair_id}")
        chair_email = c.fetchall()[0][0]
        email_list.append(chair_email)

        for panellist in room["adjudicators"]["panellists"]:
            panellist_id = panellist.split("/")[-1]
            c.execute(
                f"SELECT email FROM email_table WHERE id = {panellist_id}")
            panellist_email = c.fetchall()[0][0]
            email_list.append(panellist_email)

        for trainee in room["adjudicators"]["trainees"]:
            trainee_id = trainee.split("/")[-1]
            c.execute(f"SELECT email FROM email_table WHERE id = {trainee_id}")
            trainee_email = c.fetchall()[0][0]
            email_list.append(trainee_email)

        rooms[room_name] = email_list.copy()

    csvlist = []
    zoomnumber = math.ceil(len(rooms.keys()) / int(inputs["room_per_zoom"]))
    for x in range(zoomnumber):
        csvlist.append(csv.writer(
            open(f'round{round_number}_zoom{x+1}.csv', "w", newline='')))

    for x in csvlist:
        x.writerow(['Pre-assign Room Name', 'Email Address'])

    print(rooms)

    room_names = list(rooms.keys())
    for x in range(zoomnumber):
        for room_name in room_names[int(inputs["room_per_zoom"]) * x:int(inputs["room_per_zoom"]) * (x + 1)]:
            for email in rooms[room_name]:
                csvlist[x].writerow([room_name, email])

    conn.close()


if __name__ == "__main__":
    allocate()
