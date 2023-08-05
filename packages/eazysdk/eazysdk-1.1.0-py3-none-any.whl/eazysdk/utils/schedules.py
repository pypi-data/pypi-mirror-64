from pathlib import Path
from datetime import datetime
import json


class Schedules:
    def __init__(self, settings):
        base_path = Path(__file__).parent
        sandbox_schedules_file = (base_path / '../includes/sandbox.csv').resolve()
        ecm3_schedules_file = (base_path / '../includes/ecm3.csv').resolve()
        self.selected_file = None
        self.settings = settings

        if settings.current_environment['env'.lower()] == 'sandbox':
            self.selected_file = sandbox_schedules_file
        else:
            self.selected_file = ecm3_schedules_file

    def check_schedule_file_exists(self):
        if self.selected_file.is_file():
            return True
        else:
            return False

    def check_schedule_file_age(self):
        file = self.selected_file
        with open(file, 'r') as f:
            f.seek(0)
            try:
                data = json.load(f)
                # ISO date formatting
                date_format = '%Y-%m-%d'
                last_update_date_text = data['last_update_date']['last_updated']
                last_update_date = datetime.strptime(
                    last_update_date_text,
                    date_format,
                )
                day_difference = datetime.today() - last_update_date

                if day_difference.days > 60:
                    return True
                else:
                    return False
            except json.JSONDecodeError:
                return False

    def read_schedules_file(self):
        file = self.selected_file
        with open(file, 'r') as f:
            x = f.read()
            return x

    @staticmethod
    def format_schedule_response_as_json(resp):
        services_list = json.loads(resp)
        schedules_list = services_list['Services']
        schedules_json = {'schedule': []}
        for i in range(len(schedules_list)):
            schedules = (schedules_list[i]['Schedules'])
            for schedule in schedules:
                # Ad-hoc will appear nowhere else other than
                # potentially name. It will be in Description
                # every time, however.
                if 'AD-HOC Payments' in schedule['Description']:
                    schedule_type = False
                else:
                    schedule_type = True

                schedules_json['schedule'].append({
                    'name': schedule['Name'],
                    'ad_hoc': schedule_type,
                    'frequency': schedule['Frequency'],
                })
                # We save the date in ISO format, but JSON cannot
                # parse a date
            schedules_json['last_update_date'] = ({
                'last_updated': str(datetime.now().date())
            })
        return schedules_json

    def write_schedules_file(self, resp):
        schedule_json_object = self.format_schedule_response_as_json(resp)
        file = self.selected_file
        with open(file, 'w') as f:
            json.dump(schedule_json_object, f)
        return 'Updated schedules list.'
