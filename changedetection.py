import json

from sendNotify import mail, notify


def build_parser_from_cfg(task_cfg):
    from core.all import module_dict
    parser_cfg = task_cfg['parser']
    obj_type = parser_cfg.pop('type')
    obj_cls = module_dict[obj_type]
    return obj_cls(**parser_cfg)


def build_message_from_cfg(task_cfg):
    from message.all import module_dict
    parser_cfg = task_cfg['message']
    obj_type = parser_cfg.pop('type')
    obj_cls = module_dict[obj_type]
    return obj_cls(**parser_cfg)


"""crontab
0 6,18 * * *
"""
if __name__ == '__main__':
    should_notify = False
    with open("change_detection_tasks.json", 'r', encoding='utf-8') as f:
        tasks = json.loads(f.read())
    for i, task in enumerate(tasks):
        parser = build_parser_from_cfg(task)
        old, new = parser.parse(task['title'])
        if new:
            message = build_message_from_cfg(task).build_message(task['title'], [i[1] for i in new])
            notify(message, end='')
            should_notify = True
    if should_notify:
        mail("关注助手", "您关注的东西更新啦~")
