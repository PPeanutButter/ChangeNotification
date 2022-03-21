import json
import threading
import core
import message
from multiprocessing import Process
from Registry import module_dict
from sendNotify import qq


def build_parser_from_cfg(task_cfg):
    parser_cfg = task_cfg['parser']
    obj_type = parser_cfg.pop('type')
    obj_cls = module_dict[obj_type]
    return obj_cls(**parser_cfg)


def build_message_from_cfg(task_cfg):
    parser_cfg = task_cfg['message']
    obj_type = parser_cfg.pop('type')
    obj_cls = module_dict[obj_type]
    return obj_cls(**parser_cfg)


def merge_cfg_by_default(task_cfg):
    with open("base_tasks.json", 'r', encoding='utf-8') as fr:
        base_tasks = json.loads(fr.read())
    for k, v in base_tasks.items():
        if k not in task_cfg:
            task_cfg[k] = v
    return task_cfg


def job(_task):
    print("running ", _task['title'])
    _task = merge_cfg_by_default(_task)
    old, new = build_parser_from_cfg(_task).parse(_task['title'])
    if new:
        qq(msg_to=_task['QQ'], msg=build_message_from_cfg(_task).build_message([i for i in new]))


"""crontab
0 6,18 * * *
"""
if __name__ == '__main__':
    with open("change_detection_tasks.json", 'r', encoding='utf-8') as f:
        tasks = json.loads(f.read())
    thread_lock = threading.Semaphore(4)
    for task in tasks:
        if thread_lock.acquire():
            try:
                Process(target=job, args=(task,)).start()
            finally:
                thread_lock.release()

