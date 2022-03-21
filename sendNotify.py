import requests


def mail(title: str, subject, allMess, msg_from, password, msg_to, smtp_ssl) -> None:
    """
    使用 电子邮箱 推送消息。
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    content = allMess.replace('\n', '<br>')  # 邮件正文内容。
    msg = MIMEText(content, 'html', 'utf-8')

    msg_header = Header(title, 'utf-8')
    msg_header.append(f'<{msg_from}>', 'ascii')
    msg['Subject'] = subject
    msg['From'] = msg_header
    msg['To'] = msg_to
    client = None
    try:
        client = smtplib.SMTP_SSL(smtp_ssl, smtplib.SMTP_SSL_PORT)
        client.login(msg_from, password)
        client.sendmail(msg_from, msg_to, msg.as_string())
    except smtplib.SMTPException as e:
        print("error when send email", e)
    finally:
        if client:
            client.quit()


def qq(msg_to, msg):
    try:
        print(requests.get(url=f'http://127.0.0.1:8080/send?msg={msg}&qq={msg_to}'))
    except BaseException as e:
        print("error when send email", e)
