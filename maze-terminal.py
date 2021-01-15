import sys
import web
from doors import Doors
import feeder

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
        elif command == "toggle":
            door_number = int(querystring.split("/")[1])
            if doors.door_open[door_number]:
              doors.door_open[door_number] = False
              doors.close_door(door_number)
              return "closed"
            else: 
              doors.door_open[door_number] = True
              doors.open_door(door_number)
              return "open"
        elif command == "close":
            door_number = int(querystring.split("/")[1])
            if doors.door_open[door_number]:
              doors.door_open[door_number] = False
              doors.close_door(door_number)
            return "closed"
        elif command == "open":
            door_number = int(querystring.split("/")[1])
            if not doors.door_open[door_number]:
                doors.door_open[door_number] = True
                doors.open_door(door_number)
            return "open"
        elif command == "feeder":
            feeder.singleton.active = True
            return 'feeder enabled'
        elif command == "water":
            ms = int(querystring.split("/")[1])
            feeding_time = 1 / 1000 * ms
            feeder.singleton.feed(feeding_time)
        elif command == "end":
            sys.exit(0)
            return
        elif command == "door_status":
            door_number = int(querystring.split("/")[1])
            return "open" if doors.door_open[door_number] else "closed"
        elif command == "feeder_status":
            return "armed" if feeder.singleton.active else "disarmed"
        return 'unknown command!'

if __name__ == "__main__":
    app.run() 


