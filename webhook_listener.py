from flask import Flask, request
import git
import os

webhook_app = Flask(__name__)

@webhook_app.route('/update_server', methods=['POST'])
def webhook():
  if request.method == 'POST':
    try:
      repo_path = '/home/dmikes/flask'
      repo = git.Repo(repo_path)
      origin = repo.remotes.origin
      origin.fetch('main')
      repo.git.reset('--hard', 'origin/main')

    except git.exc.GitCommandError as e:
      print(f'Error occurred: {e}')
      return 'Update failed', 500

    wsgi_file = '/var/www/dmikes_eu_pythonanywhere_com_wsgi.py'
    os.utime(wsgi_file, None)

    return 'PythonAnywhere updated', 200

  return 'Event type wrong', 400

if __name__ == '__main__':
  webhook_app.run()
