import requests
import json


class Deadline:
    def __init__(self, date, course, description, opportunity, meta):
        self.date = date
        self.course = course
        self.description = description
        self.opportunity = opportunity
        self.meta = meta


class Lesson:
    def __init__(self, start, end, course, location, teacher, meta):
        self.start = start
        self.end = end
        self.course = course
        self.location = location
        self.teacher = teacher
        self.meta = meta


class Meta:
    def __init__(self, last_update, user):
        self.last_update = last_update
        self.user = user


class APIConnection:
    def __init__(self, key):
        self.base_url = 'https://app.zuydbot.cc/api/v2'
        self.key = key
        self.deadlines = None
        self.lessons = None
        self.test_connection()

    def test_connection(self):
        try:
            r = requests.get(self.base_url, timeout=15)
        except requests.exceptions.ReadTimeout:
            raise TimeoutError('Connected timed out.')
        if r.status_code is not 200:
            raise ConnectionError('Cannot reach API (HTTP {}).'.format(r.status_code))

    def send_request(self, module):
        try:
            r = requests.get('{}/{}'.format(self.base_url, module), headers={'key': self.key}, timeout=15)
        except requests.exceptions.ReadTimeout:
            raise TimeoutError('Connected timed out.')
        if r.status_code is not 200:
            raise ConnectionError('Cannot reach API (HTTP {}).'.format(r.status_code))
        response = json.loads(r.content.decode('utf-8'))
        return response['deadlines'], response['meta']

    def get_deadlines(self):
        deadlines, meta = self.send_request('deadlines')
        deadline_list = []
        metadata = Meta(last_update=meta['last-update'], user=meta['user'])
        for deadline in deadlines:
            deadline_list.append(Deadline(date=deadline['date'], course=deadline['course'], meta=metadata,
                                          description=deadline['description'], opportunity=deadline['opportunity']))
        self.deadlines = deadline_list

    def get_lessons(self):
        lessons, meta = self.send_request('lessons')
        lesson_list = []
        metadata = Meta(last_update=meta['last-update'], user=meta['user'])
        for lesson in lessons:
            lesson_list.append(Lesson(start=lesson['start-time'], end=lesson['end-time'], course=lesson['course'],
                                      location=lesson['location'], teacher=lesson['teacher'], meta=metadata))
        self.lessons = lesson_list
