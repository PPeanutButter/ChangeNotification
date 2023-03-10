import hashlib
import json
import os
import re
import requests

from changedetection import home


class BaseParser:
    def __init__(self, selects):
        try:
            self.regex
        except AttributeError:
            self.regex = ".*"
        self.selects = selects

    def parse(self, task_title):
        if os.path.exists(home('task_data_store.json')):
            with open(home('task_data_store.json'), 'r', encoding='utf-8') as f:
                task_data_store = json.loads(f.read())
        else:
            task_data_store = {}
        if task_title not in task_data_store:
            task_data_store[task_title] = []
        old, new = [], []
        for selected in self.selects:
            tid = self.get_id(selected)
            if tid and re.search(self.regex, tid):
                md5 = self.get_md5(tid) + " " + tid[:100]
                if md5 not in task_data_store[task_title]:
                    task_data_store[task_title].append(md5)
                    name = self.get_name(selected)
                    new.append(name)
                else:
                    old.append(tid)
        with open(home('task_data_store.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(task_data_store, ensure_ascii=False, indent=4))
        return old, new

    @staticmethod
    def get(url):
        return requests.request('GET', url=url, headers={"Accept-Encoding": "none"}).text

    def get_id(self, selected) -> str:
        pass

    def get_name(self, selected) -> str:
        pass

    @staticmethod
    def get_md5(id):
        return hashlib.md5(id.encode('utf8')).hexdigest()
