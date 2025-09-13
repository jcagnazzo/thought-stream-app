from flask import Flask, Response, stream_with_context
import os
import random
import time
import json

try:
    import openai
except ImportError:
    openai = None

app = Flask(__name__)

FALLBACK_THOUGHTS = [
    'What if AI could dream?',
    'If you could talk to trees, what would you ask?',
    'Is there a rhythm to the noise around us?',
    'Do thoughts have weight?',
    'If life is a song, what is your key?',
]

def get_thought():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and openai:
        openai.api_key = api_key
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': 'One short poetic thought'}],
                max_tokens=20,
                temperature=0.7,
            )
            return resp['choices'][0]['message']['content'].strip()
        except Exception:
            pass
    return random.choice(FALLBACK_THOUGHTS)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
  <head>
    <title>Thought Stream</title>
  </head>
  <body>
    <h1>Thought Stream</h1>
    <ul id='thoughts'></ul>
    <script>
      const ul = document.getElementById('thoughts');
      const evtSource = new EventSource('/stream');
      evtSource.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const li = document.createElement('li');
        li.textContent = data.thought;
        ul.appendChild(li);
        window.scrollTo(0, document.body.scrollHeight);
      };
    </script>
  </body>
</html>
'''

@app.route('/stream')
def stream():
    def generate():
        while True:
            thought = get_thought()
            msg = json.dumps({'thought': thought})
            yield f'data: {msg}\\n\\n'
            delay = random.expovariate(0.5)
            time.sleep(delay)
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
