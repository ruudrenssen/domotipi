class Schedules():
    name = ''
    description = ''
    database = {}

    def __init__(self, database):
        self.database = database

    def sync_schedules(self, schedules):
        # print(schedules.__dir__())
        # print(schedules.values())
        for schedule in schedules.values():
            # weekly time shedule:
            # monday = 64, tuesday = 32, wednesday = 16, thursday = 8, friday = 4, saturday = 2, sunday = 1
            # example:
            # only on workdays, the value would be W124. (64+32+16+8+4 = 124)

            # print(schedule.__dir__())
            print(schedule)
            # print('name: ' + schedule['name'])
            # print('description: ' + schedule['description'])
            # # print('command/address: ' + schedule['command']['address'])
            # # print('command/body: ' + schedule['command']['body'])
            # # print('command/method: ' + schedule['command']['method'])
            # print('localtime: ' + schedule['localtime'])
            # print('time: ' + schedule['time'])
            # print('created: ' + schedule['created'])
            # print('status: ' + str(schedule['status']))
            # print('autodelete: ' + str(schedule['autodelete']))
            # if schedule['starttime']:
            #     print('starttime: ' + schedule['starttime'])
            # print('recycle: ' + str(schedule['recycle']))
            pass

