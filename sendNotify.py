import json
import logging
import threading

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)

# 配信内容格式
allMess = ''
mutex = threading.Lock()


def notify(content=None, end='\n'):
    with mutex:
        global allMess
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        allMess = allMess + content + end
        logger.info(content)


def console() -> None:
    """
    使用 控制台 推送消息。
    """
    with open('log.log', 'r+', encoding='utf-8') as f:
        content_old = f.read()
        f.seek(0, 0)
        f.write(allMess + content_old)


def mail(title: str, subject="树莓派薅羊毛脚本") -> None:
    """
    使用 电子邮箱 推送消息。
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    msg_from = '290120506@qq.com'  # 发送方邮箱地址。
    password = ""  # 发送方QQ邮箱授权码，不是QQ邮箱密码。

    # subject = "体温填报"  # 主题。
    content = allMess.replace('\n', '<br>')  # 邮件正文内容。
    msg = MIMEText(content, 'html', 'utf-8')

    msg_header = Header(title, 'utf-8')
    msg_header.append('<290120506@qq.com>', 'ascii')
    msg_to = "panrunqiu@outlook.com"
    msg['Subject'] = subject
    msg['From'] = msg_header
    msg['To'] = msg_to
    client = None
    try:
        client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        client.login(msg_from, password)
        client.sendmail(msg_from, msg_to, msg.as_string())
    except smtplib.SMTPException as e:
        print("error when send email", e)
    finally:
        if client:
            client.quit()


def send(title: str, content: str) -> None:
    if not content:
        print(f"{title} 推送内容为空！")
        return
    console()


def save() -> None:
    console()


def main():
    send("title", "content")


if __name__ == "__main__":
    main()
