class Schedules:
    name = ''
    description = ''
    database = {}

    def __init__(self, database):
        self.database = database

    @staticmethod
    def sync_schedules(schedules):
        # print(schedules.__dir__())
        # print(schedules.values())
        # print(schedule)

        for schedule in schedules.values():
            # filter starting points schedules
            # print(schedule)
            if 'scene' in schedule['command']['body']:
                print(schedule['command']['address'])
                # if schedule['command']['body']['flag']:
                #     pass
                    # print('name: ' + schedule['name'] + ', ' + schedule['description'])
                    # print('starttime: ' + schedule['starttime'])






            # print(schedule.__dir__())
            # print('description: ' + schedule['description'])
            # print('command/address: ' + schedule['command']['address'])
            # print('command/body: ' + schedule['command']['body'])
            # print('command/body: ' + schedule['command']['body']['scene'])
            # if 'scene' in schedule['command']['body']:
            #     print('name: ' + schedule['name'])
            #     print('command/body: ' + schedule['command']['body']['scene'])
            # print('command/method: ' + schedule['command']['method'])
            # print('localtime: ' + schedule['localtime'])
            # print('time: ' + schedule['time'])
            # print('created: ' + schedule['created'])
            # print('status: ' + str(schedule['status']))
            # print('autodelete: ' + str(schedule['autodelete']))
            # if schedule['starttime']:
            #     print('starttime: ' + schedule['starttime'])
            # print('recycle: ' + str(schedule['recycle']))
            pass

    @staticmethod
    def get_week_pattern(schedule):
        # weekly time format:
        # monday = 64, tuesday = 32, wednesday = 16, thursday = 8, friday = 4, saturday = 2, sunday = 1
        # example:
        # only on workdays, the value would be W124. (64+32+16+8+4 = 124)

        days_of_the_week = [
            {'name': 'monday', 'value': 64},
            {'name': 'tuesday', 'value': 32},
            {'name': 'wednesday', 'value': 16},
            {'name': 'thursday', 'value': 8},
            {'name': 'friday', 'value': 4},
            {'name': 'saturday', 'value': 2},
            {'name': 'sunday', 'value': 1},
        ]

        schedule = 124

        for day in days_of_the_week:
            print(day['name'])
