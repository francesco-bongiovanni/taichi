import taichi as tc
import smtplib
import os
import socket
import atexit

gmail_sender = 'taichi.messager@gmail.com'
gmail_passwd = '6:L+XbNOp^'

emailed = False


def send_crash_report(message, receiver=None):
  global emailed
  if emailed:
    return
  emailed = True
  if receiver is None:
    receiver = os.environ.get('TC_MONITOR_EMAIL', None)
  if receiver is None:
    tc.warning('No receiver in $TC_MONITOR_EMAIL')
    return
  tc.warning('Emailing {}'.format(receiver))
  TO = receiver
  SUBJECT = 'Report'
  TEXT = message

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login(gmail_sender, gmail_passwd)

  BODY = '\r\n'.join([
      'To: %s' % TO,
      'From: %s' % gmail_sender,
      'Subject: %s' % SUBJECT, '', TEXT
  ])

  try:
    server.sendmail(gmail_sender, [TO], BODY)
  except:
    print('Error sending mail')
  server.quit()
  print('Press enter or Ctrl + \ to exit.')


def enable(task_name):
  register_call_back(task_name)


crashed = False
keep = []


def register_call_back(task_name):

  def at_exit():
    if not crashed:
      message = 'Congratulations! Your task [{}] at machine [{}] has finished.'.format(
          task_name, socket.gethostname())
      send_crash_report(message)

  def email_call_back(_):
    global crashed
    crashed = True
    tc.warning('Task has crashed.')
    message = 'Your task [{}] at machine [{}] has crashed.'.format(
        task_name, socket.gethostname())
    send_crash_report(message)
    atexit.unregister(at_exit)
    exit(-1)

  keep.append(email_call_back)
  call_back = tc.function11(email_call_back)
  tc.core.register_at_exit(call_back)

  atexit.register(at_exit)


if __name__ == '__main__':
  register_call_back('test')
  tc.core.trigger_sig_fpe()
