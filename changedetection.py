import json
import core
import message
from Registry import module_dict
from sendNotify import mail


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


"""crontab
0 6,18 * * *
"""
if __name__ == '__main__':
    with open("change_detection_tasks.json", 'r', encoding='utf-8') as f:
        tasks = json.loads(f.read())
    for i, task in enumerate(tasks):
        task = merge_cfg_by_default(task)
        old, new = build_parser_from_cfg(task).parse(task['title'])
        if new:
            message = build_message_from_cfg(task).build_message([i[1] for i in new])
            print(message)
            mail(task['title'], "关注助手", allMess=message, msg_from=task['EmailFrom'],
                 msg_to=task['EmailTo'], password=task['EmailPassword'],
                 smtp_ssl=task['SMTP_SSL'])
