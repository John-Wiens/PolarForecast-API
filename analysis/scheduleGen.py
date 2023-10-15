import simulator as sim




teams = {
        1339:None,
        1410:None,
        1619:None,
        1799:None,
        1977:None,
        2036:None,
        2083:None,
        2240:None,
        2972:None,
        2996:None,
        3200:None,
        3374:None,
        3729:None,
        3807:None,
        4068:None,
        4293:None,
        4418:None,
        4499:None,
        4550:None,
        4944:None,
        5493:None,
        5933:None,
        7485:None,
        8334:None,
        4388:None,
        9339:None,
        9338:None,
        9337:None,
        9336:None,
        9335:None,
        9334:None,
        9333:None,
        9332:None,
        9998:None,
        9331:None,
        9999:None,
        9329:None,
        9330:None,
        }

schedule = sim.get_random_schedule(teams, 72)

count = 1
for match in schedule:
    alliances = match.get('alliances')
    red = alliances.get('red').get("team_keys")
    blue = alliances.get('blue').get("team_keys")

    print(count, red[0],red[1],red[2],blue[0],blue[1],blue[2])
    
    count +=1
