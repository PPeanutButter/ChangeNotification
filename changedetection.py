import argparse
import json
import os
import sys
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
    with open(home("base_tasks.json"), 'r', encoding='utf-8') as fr:
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


def home(path):
    return os.path.join(sys.path[0], path)


"""crontab
0 6,18 * * *
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--show_cfg', action='store_true', help='打印支持的解析器与消息发送器')
    parser.add_argument('--show_tasks', action='store_true', help='打印所有任务')
    parser.add_argument('--show_tasks_', action='store_true', help='打印所有被禁用的任务')
    parser.add_argument('--show_records', action='store_true', help='打印所有任务记录')
    parser.add_argument('--with_readable', action='store_true', help='格式化json')
    args = parser.parse_args()
    if args.show_cfg:
        with open(home('doc.json'), mode='r', encoding='utf-8') as f:
            doc = json.loads(f.read())
        _p = []
        _m = []
        for k, v in module_dict.items():
            r = {}
            if k in doc:
                r[k] = doc[k]
                if str(k).endswith("Parser"):
                    _p.append(r)
                else:
                    _m.append(r)
        print(json.dumps(dict(parser=_p, messager=_m), ensure_ascii=False, indent=4 if args.with_readable else None))
        sys.exit(0)
    with open(home("change_detection_tasks.json"), 'r', encoding='utf-8') as f:
        tasks = json.loads(f.read())
        if args.show_tasks:
            print(json.dumps(tasks, ensure_ascii=False, indent=4 if args.with_readable else None))
            sys.exit(0)
    if args.show_tasks_:
        with open(home("_change_detection_tasks.json"), 'r', encoding='utf-8') as f:
            print(json.dumps(json.loads(f.read()), ensure_ascii=False, indent=4 if args.with_readable else None))
            sys.exit(0)
    if args.show_records:
        if os.path.exists(home('task_data_store.json')):
            with open(home('task_data_store.json'), 'r', encoding='utf-8') as f:
                task_data_store = json.loads(f.read())
                print(json.dumps(task_data_store, ensure_ascii=False, indent=4 if args.with_readable else None))
        else:
            print("{}")
        sys.exit(0)

    if args.debug:
        for task in tasks:
            job(task)
    else:
        thread_lock = threading.Semaphore(4)
        for task in tasks:
            if thread_lock.acquire():
                try:
                    Process(target=job, args=(task,)).start()
                finally:
                    thread_lock.release()
