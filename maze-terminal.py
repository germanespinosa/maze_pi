import sys
import web
from doors import Doors
import feeder
import json

doors = Doors()

urls = (
    '/(.*)', 'maze_terminal'
)
app = web.application(urls, globals())

class maze_terminal:
    def GET(self, querystring):
        print ("querystring: ", querystring)
        command = querystring.split("/")[0]
        if command == "servo":
            door_number = int(querystring.split("/")[1])
            value = querystring.split("/")[2]
            return doors.door_feed(door_number,float(value))
        elif command == "status":
            response = {"code":0, "message" : "Ok"}
            response["content"] = {}
            response["content"]["door_status"] = doors.status()
            response["content"]["feeder_status"] = feeder.singleton.status()
            return json.dumps(response)
        elif command == "toggle":
            door_number = int(querystring.split("/")[1])
            if doors.door_open[door_number]:
                doors.door_open[door_number] = False
                doors.close_door(door_number)
                response = {"code": 0, "message": "door closed"}
                return json.dumps(response)
            else: 
              doors.door_open[door_number] = True
              doors.open_door(door_number)
              response = {"code": 0, "message": "door opened"}
              return json.dumps(response)
        elif command == "close":
            door_number = int(querystring.split("/")[1])
            if doors.door_open[door_number]:
                doors.door_open[door_number] = False
                doors.close_door(door_number)
                response = {"code": 0, "message": "door closed"}
                return json.dumps(response)
            response = {"code": 1, "message": "door already closed"}
            return json.dumps(response)
        elif command == "open":
            door_number = int(querystring.split("/")[1])
            if not doors.door_open[door_number]:
                doors.door_open[door_number] = True
                doors.open_door(door_number)
                response = {"code": 0, "message": "door opened"}
                return json.dumps(response)
            response = {"code": 1, "message": "door already open"}
            return json.dumps(response)
        elif command == "enable_feeder":
            feeder.singleton.active = True
            response = {"code": 0, "message": "feeder enabled"}
            return json.dumps(response)
        elif command == "test_feeder":
            ms = int(querystring.split("/")[1])
            reps = int(querystring.split("/")[2])
            wait = int(querystring.split("/")[3])
            feeding_time = 1 / 1000 * ms
            feeder.singleton.test(feeding_time, reps, wait)
            response = {"code": 0, "message": "test finished"}
            return json.dumps(response)
        elif command == "calibrate_feeder":
            ms = int(querystring.split("/")[1])
            feeding_time = 1 / 1000 * ms
            feeder.singleton.save_calibration(feeding_time)
            response = {"code": 0, "message": "clibration saved"}
            return json.dumps(response)
        elif command == "water":
            ms = int(querystring.split("/")[1])
            feeding_time = 1 / 1000 * ms
            feeder.singleton.feed(feeding_time)
            response = {"code": 0, "message": "water delivered"}
            return json.dumps(response)
        elif command == "end":
            global app
            app.stop()
            response = {"code": 0, "message": "good bye"}
            return json.dumps(response)
        return 'unknown command!'

if __name__ == "__main__":
    app.run() 


