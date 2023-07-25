#!/usr/bin/python3

import requests
import json
import sys
import time

url = "https://gql-realtime-2.reddit.com/query"


def convertX(x: int, canvasId: int) -> int:
    canvasId = canvasId % 3
    return (x + 1500) - ((canvasId)*1000)


def convertY(y: int, canvasId: int) -> int:
    if canvasId > 3:
        return y
    else:
        return 1000 + y


def getCanvasIndex(x: int, y: int) -> int:
    x = 1500 + x
    if y >= 0:
        if x >= 0 and x < 1000:
            return 3
        if x >= 1000 and x < 2000:
            return 4
        if x >= 2000 and x < 3000:
            return 5
    else:
        if x >= 0 and x < 1000:
            return 0
        if x >= 1000 and x < 2000:
            return 1
        if x >= 2000 and x < 3000:
            return 2


def getColorId(color: str) -> int:
    colorPalatte = {"red": 2,
                    "orange": 3,
                    "yellow": 4,
                    "dark_green": 6,
                    "light_green": 8,
                    "dark_blue": 12,
                    "blue": 13,
                    "light_blue": 14,
                    "dark_purple": 18,
                    "purple": 19,
                    "light_pink": 23,
                    "brown": 25,
                    "black": 27,
                    "gray": 29,
                    "light_gray": 30,
                    "white": 31
                    }
    try:
        return colorPalatte[color]
    except:
        return -1


def getHeaders(authToken: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "authorization": f"Bearer {authToken}"
    }
    return headers


def setPixel(x: int, y: int, colorId: int, canvasId: int, authToken: str):
    request_data = {
        "operationName": "setPixel",
        "variables": {
            "input": {
                "actionName": "r/replace:set_pixel",
                "PixelMessageData": {
                    "coordinate": {"x": x, "y": y},
                    "colorIndex": colorId,
                    "canvasIndex": canvasId
                }
            }
        },
        "query": "mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    print(f"Placing pixel at x:{x}, y:{y} with color id {colorId}")
    res = requests.post(url, headers=getHeaders(authToken), json=request_data)
    # print(res.text)
    resJ = json.loads(res.text)
    if "errors" not in resJ:
        return (resJ["data"]["act"]["data"][0]["data"]["nextAvailablePixelTimestamp"], True)
    if "extensions" not in resJ["errors"][0]:
        return (sys.maxsize, False)
    return (resJ["errors"][0]["extensions"]["nextAvailablePixelTs"], False)


def getPixelDetail(x: int, y: int, colorId: int, canvasId: int, authToken: str):
    request_data = {
        "operationName": "pixelHistory",
        "variables": {
            "input": {
                "actionName": "r/replace:get_tile_history",
                "PixelMessageData": {
                    "coordinate": {"x": x, "y": y},
                    "colorIndex": 0,
                    "canvasIndex": canvasId
                }
            }
        },
        "query": "mutation pixelHistory($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetTileHistoryResponseMessageData {\n            lastModifiedTimestamp\n            userInfo {\n              userID\n              username\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    res = requests.post(url, headers=getHeaders(authToken), json=request_data)
    return res.text


def setCoolDownTime(x: int, y: int, colorId: int, canvasId: int, authToken: str) -> str:

    request_data = {
        "query": "mutation GetPersonalizedTimer{\n  act(\n    input: {actionName: \"r/replace:get_user_cooldown\"}\n  ) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n          }\n        }\n      }\n    }\n  }\n}\n\n\nsubscription SUBSCRIBE_TO_CONFIG_UPDATE {\n  subscribe(input: {channel: {teamOwner: GARLICBREAD, category: CONFIG}}) {\n    id\n    ... on BasicMessage {\n      data {\n        ... on ConfigurationMessageData {\n          __typename\n          colorPalette {\n            colors {\n              hex\n              index\n            }\n          }\n          canvasConfigurations {\n            dx\n            dy\n            index\n          }\n          canvasWidth\n          canvasHeight\n        }\n      }\n    }\n  }\n}\n\n\nsubscription SUBSCRIBE_TO_CANVAS_UPDATE {\n  subscribe(\n    input: {channel: {teamOwner: GARLICBREAD, category: CANVAS, tag: \"0\"}}\n  ) {\n    id\n    ... on BasicMessage {\n      id\n      data {\n        __typename\n        ... on DiffFrameMessageData {\n          currentTimestamp\n          previousTimestamp\n          name\n        }\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n      }\n    }\n  }\n}\n\n\n\n\nmutation SET_PIXEL {\n  act(\n    input: {actionName: \"r/replace:set_pixel\", PixelMessageData: {coordinate: { x: 53, y: 35}, colorIndex: 3, canvasIndex: 0}}\n  ) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on SetPixelResponseMessageData {\n            timestamp\n          }\n        }\n      }\n    }\n  }\n}\n\n\n\n\n# subscription configuration($input: SubscribeInput!) {\n#     subscribe(input: $input) {\n#       id\n#       ... on BasicMessage {\n#         data {\n#           __typename\n#           ... on RReplaceConfigurationMessageData {\n#             colorPalette {\n#               colors {\n#                 hex\n#                 index\n#               }\n#             }\n#             canvasConfigurations {\n#               index\n#               dx\n#               dy\n#             }\n#             canvasWidth\n#             canvasHeight\n#           }\n#         }\n#       }\n#     }\n#   }\n\n# subscription replace($input: SubscribeInput!) {\n#   subscribe(input: $input) {\n#     id\n#     ... on BasicMessage {\n#       data {\n#         __typename\n#         ... on RReplaceFullFrameMessageData {\n#           name\n#           timestamp\n#         }\n#         ... on RReplaceDiffFrameMessageData {\n#           name\n#           currentTimestamp\n#           previousTimestamp\n#         }\n#       }\n#     }\n#   }\n# }\n",
        "variables": {
            "input": {
                "channel": {
                    "teamOwner": "GARLICBREAD",
                    "category": "R_REPLACE",
                    "tag": "canvas:0:frames"
                }
            }
        },
        "operationName": "GetPersonalizedTimer",
        "id": None
    }

    res = requests.post(url, headers=getHeaders(authToken), json=request_data)
    # print(res.text)
    resJ = json.loads(res.text)
    # print(resJ)
    if "errors" not in resJ:
        cool = resJ["data"]["act"]["data"][0]["data"]["nextAvailablePixelTimestamp"]
        if cool == None:
            return 0
        return cool
    return sys.maxsize


def main():
    data = {}
    try:
        with open("data.json") as f:
            data = json.loads(f.read())
        if len(data["accounts"]) <= 0:
            print("Provide accounts auth token")
            return
        print(
            f"fetching the cooldown time of all accounts => {len(data['accounts'])}")
        for acc in data["accounts"]:
            if "cooldown" not in acc:
                cId = getCanvasIndex(
                    data["pixels"][0]["x"], data["pixels"][0]["y"])
                acc["cooldown"] = setCoolDownTime(convertX(data["pixels"][0]["x"], cId), convertY(
                    data["pixels"][0]["y"], cId), getColorId(data["pixels"][0]["color"]), cId, acc["auth"])
            print(f"User: {acc['username']} Cooldown: {acc['cooldown']}")
    except Exception as e:
        print("Unable to read file", e)
        return

    if len(data["pixels"]) <= 0:
        print("No pixels provided")
        return
    print("Placing of tiles started")
    while True:
        i = 0
        while i < len(data["pixels"]):
            curP = data["pixels"][i]
            available_acc = sorted(
                data["accounts"], key=lambda x: int(x["cooldown"]), reverse=False)[0]

            userlist = [i['username'] for i in data['accounts']]

            if available_acc["cooldown"] > (time.time()*1000):
                secs = (available_acc["cooldown"] - (time.time()*1000))/1000
                print(
                    f"sleeping until the cooltime {secs//60} mins and {(secs%60)} secs")
                time.sleep(secs)
                continue

            canvasId = getCanvasIndex(curP["x"], curP["y"])

            colorId = getColorId(curP["color"])

            if colorId == -1:
                print("wronge color provide correct color wronge pixel data")
                i += 1
                continue

            x = convertX(curP["x"], canvasId)
            y = convertY(curP["y"], canvasId)
            print(f"Checking {curP['x'], curP['y']}")

            targetPixel = getPixelDetail(
                x, y, 0, canvasId, available_acc["auth"])
            targetPixel = json.loads(targetPixel)
            targetPixelOwner = targetPixel['data']['act']['data'][0]['data']['userInfo']['username']

            print(
                f"The target pixel is currently owned by {targetPixelOwner}")

            if targetPixelOwner in userlist:
                print("we already own this pixel skip")
                res = True
                cooldown = 0
            else:
                cooldown, res = setPixel(
                    x, y, colorId, canvasId, available_acc["auth"])

                print(
                    f"{available_acc['username']} has just tried to place a pixel at {curP['x']}, {curP['y']}")

                time.sleep(30)
            if res:
                available_acc["cooldown"] = int(cooldown)
                i += 1
                continue
            available_acc["cooldown"] = int(cooldown)


if __name__ == "__main__":
    main()
