# happy-beer-bot
Sample app using Bolt for Python for "Dev Velocity" meetup (May 2022)

Based on the slack documentation:  
https://api.slack.com/start/building/bolt-python  
https://slack.dev/bolt-python/concepts  
https://github.com/slackapi/bolt-python  

Bolt is a foundational framework that makes it easier to build Slack apps with the platform's latest features. This guide walks you through building your first app with [Bolt for Python](https://slack.dev/bolt-python/concepts).

Along the way, you'll create a new Slack app, set up a simple development environment, and build an app that listens and responds to events from your Slack workspace.
- [Getting started](#getting-started)
  - [Creating a Slack app](#creating-a-slack-app)
  - [Requesting scopes](#requesting-scopes)
  - [Installing your app](#installing-your-app)
- [Configuring your local environment](#configuring-your-local-environment)
  - [Create a virtual environment](#create-a-virtual-environment)
  - [Adding your app credentials](#adding-your-app-credentials)
  - [Using ngrok as a local proxy](#using-ngrok-as-a-local-proxy)
- [Developing your app](#developing-your-app)
- [Subscribing to events](#subscribing-to-events)
- [Responding to events](#responding-to-events)

# Getting started 
This README covers creating a basic Slack app tailored to work with Bolt. There is a more general [app setup](https://api.slack.com/authentication/basics) guide that goes into greater detail.

## Creating a Slack app
To get started, you'll need to create a new Slack app (create a Slack app [here](https://api.slack.com/apps?new_app=1&ref=bolt_start_hub)).

Fill out your **App Name** and select the **Development Workspace** where you'll play around and build your app. You'll still be able to [distribute your app](https://api.slack.com/start/distributing/public) to other workspaces if you choose.

## Requesting scopes 
[Scopes](https://api.slack.com/scopes) give your app permission (for example, post messages). Go to the **OAuth & Permissions** sidebar:

Scroll down to the **Bot Token Scopes** section and click **Add an OAuth Scope**.

For now, we'll only use one scope. Add the **chat:write** scope to grant your app the permission to post messages in channels it's a member of.

## Installing your app 
Install your own app by selecting the **Install App** button at the top of the **OAuth & Permissions** page, or from the sidebar.

After clicking through one more green **Install App To Workspace** button, you'll be sent through the Slack OAuth UI.
After the installation, you'll land back in the **OAuth & Permissions** page and find a **Bot User OAuth Access Token**.

Access tokens are imbued with power. They represent the permissions delegated to your app by the installing user. Remember to keep your access token secret and safe, to avoid violating the trust of the installing user.

At a minimum, avoid checking your access token into public version control. Access it via an environment variable. There are plenty more [best practices for app security](https://api.slack.com/authentication/best-practices).

# Configuring your local environment 
## Create a virtual environment
```bash
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install slack_bolt
```

## Adding your app credentials 
Copy the **Bot User OAuth Access Token** under the **OAuth & Permissions** sidebar (talked about in the [installation section](#installing-your-app)).

Export your token as `SLACK_BOT_TOKEN`:
```bash
export SLACK_BOT_TOKEN=xoxb-your-token
````
Navigate to the **Basic Information** page from your app management page. Under **App Credentials**, copy the value for **Signing Secret**.

Export your signing secret as `SLACK_SIGNING_SECRET`:
```bash
export SLACK_SIGNING_SECRET=your-signing-secret
````


## Using ngrok as a local proxy 
To develop locally we'll be using **ngrok**, which allows you to expose a public endpoint that Slack can use to send your app events. If you haven't already, [install ngrok from their website](https://ngrok.com/download).

If you haven't used ngrok before, read our full tutorial for a more in-depth walkthrough on [using ngrok to develop locally](https://api.slack.com/tutorials/tunneling-with-ngrok).

Use ngrok with port 3000 (which Bolt for Python uses by default):
```bash
ngrok http 3000
````

# Developing your app

Create a Bolt for Python app by calling a constructor, which is a top-level export. If you'd prefer, you can create an [async app](#creating-an-async-app).
After you've installed the slack_bolt package and added your app credentials, create a new app.py file and paste the following:
```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.action("yes_button") etc


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))  # POST http://localhost:3000/slack/events
```

## Running the app
The above code initializes the app using the `App` constructor, then starts a simple HTTP server on port 3000. The HTTP server is using a built-in development adapter, which is responsible for handling and parsing incoming events from Slack. You can run your app now, but it won't do much.

```bash
# export the slack token and secret if you have not sone it in the earlier steps
export SLACK_SIGNING_SECRET=your-signing-secret
export SLACK_BOT_TOKEN=xoxb-your-token

# run the app
python app.py

# in another terminal (if it isn't running already)
ngrok http 3000
```
