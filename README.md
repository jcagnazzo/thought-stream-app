# Thought Stream App

This small Flask application streams a constant stream of short "thoughts" to the browser using Server-Sent Events (SSE). It can be used stand‑alone with a few random fallback phrases or integrated with the OpenAI API to generate a more diverse stream of thoughts.

## Features

- HTTP endpoint /stream that emits a never-ending stream of JSON messages containing snippets of "thoughts" with random delays.
- Optional integration with the OpenAI API: set OPENAI_API_KEY in your environment and the app will query gpt-3.5-turbo for new thoughts.
- Exponential backoff: inter-arrival times of thoughts follow an exponential distribution, simulating natural thought bursts.
- Minimal front end: open http://localhost:5000 to start listening.

## Quickstart

1. Install the dependencies: pip install -r requirements.txt
2. Run the server: python app.py
3. Open http://localhost:5000 in your browser to see the stream of thoughts.

If you wish to enable the OpenAI integration, set the OPENAI_API_KEY environment variable before running the app.

## Deployment

This repo includes a Procfile for deploying to Heroku with Gunicorn. To deploy:

1. Create a new Heroku app (e.g., thought-stream-app) and add your OPENAI_API_KEY (optional) as a config variable.
2. Connect your Heroku app to this GitHub repository.
3. Trigger a deploy from the Heroku dashboard.

The requirements.txt and Procfile are configured for Python 3 and Gunicorn. There are no database dependencies.
