#!/usr/bin/python3

import requests
import json
import sys
import time

url = "https://gql-realtime-2.reddit.com/query"

def convertX(x:int,canvasId:int)->int:
    canvasId = canvasId % 3
    return (x + 1500) - ((canvasId)*1000)

def convertY(y:int,canvasId:int)->int:
    if canvasId > 3 :
        return y
    else :
        return 1000 +  y

def getCanvasIndex(x:int,y:int)->int:
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

def getColorId(color:str)->int:
    colorPalate = {"red":2,"blue":13,"white":31,"green":6,"black":27,"yellow":4,"orange":3,"purple":19}
    try :
        return colorPalate[color]
    except:
        return -1

def setPixel(x:int,y:int,colorId:int,canvasId:int,authToken:str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "authorization": f"Bearer {authToken}"
    }
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

    res = requests.post(url, headers=headers,json=request_data)
    resJ = json.loads(res.text)
    if "errors" not in resJ:
        return(resJ["data"]["act"]["data"][0]["data"]["nextAvailablePixelTimestamp"],True)
    # print(resJ)
    return (resJ["errors"][0]["extensions"]["nextAvailablePixelTs"],False)

def getPixelDetail(x:int,y:int,colorId:int,canvasId:int,authToken:str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "authorization": f"Bearer {authToken}"
    }
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

    res = requests.post(url, headers=headers,json=request_data)
    return res.text


def setCoolDownTime(x:int,y:int,colorId:int,canvasId:int,authToken:str)->str:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "authorization": f"Bearer {authToken}"
    }
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

    res = requests.post(url, headers=headers,json=request_data)
    resJ = json.loads(res.text)
    if "errors" not in resJ:
        return resJ["data"]["act"]["data"][0]["data"]["nextAvailablePixelTimestamp"]
    return resJ["errors"][0]["extensions"]["nextAvailablePixelTs"]

def main():
    data = {}
    try :
        with open("data.json") as f:
            data = json.loads(f.read())
        if len(data["accounts"]) <= 0:
            print("Provide accounts auth token")
            return
        for acc in data["accounts"]:
            if "cooldown" not in acc :
                cId = getCanvasIndex(data["pixels"][0]["x"],data["pixels"][0]["y"])
                acc["cooldown"] = setCoolDownTime(convertX(data["pixels"][0]["x"],cId),convertY(data["pixels"][0]["y"],cId),getColorId(data["pixels"][0]["color"]),cId,acc["auth"])
    except Exception as e:
        print("Unable to read file",e)
        return

    if len(data["pixels"]) <= 0:
        print("No pixels provided")
        return
    
    while True:
        i = 0
        while i < len(data["pixels"]):
            curP = data["pixels"][i]
            available_acc = sorted(data["accounts"],key=lambda x : int(x["cooldown"]))[0]

            if available_acc["cooldown"] > (time.time()*1000) :
                secs = (available_acc["cooldown"] - (time.time()*1000))/1000
                print(f"sleeping until the cooltime {secs//60} mins and {(secs%60)} secs")
                time.sleep(secs)
                continue

            canvasId = getCanvasIndex(curP["x"],curP["y"])
            
            colorId = getColorId(curP["color"])
            if colorId == -1:
                print("wronge color provide correct color wronge pixel data")
                i += 1
                continue

            x = convertX(curP["x"],canvasId)
            y = convertY(curP["y"],canvasId)


            cooldown , res = setPixel(x,y,colorId,canvasId,available_acc["auth"])
            if res:
                available_acc["cooldown"] = int(cooldown)
                i += 1
                continue
            available_acc["cooldown"] = int(cooldown)


if __name__ == "__main__":
    main()


