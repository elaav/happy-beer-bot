# Happy Beer Bot
A sample app using Python Bolt for "Dev Velocity" meetup (May 2022)

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
- [Running the app](#running-the-app)
- [Subscribing to events](#subscribing-to-events-and-actions)
  - [Events](#events)
  - [Actions](#actions)
- [Responding to events](#responding-to-events-and-actions)
- [Slack interactive messages](#slack-interactive-messages)
  - [Messages builder](#messages-builder)
  - [Building with Block Kit](#building-with-block-kit)
  

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

# Running the app
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

# Subscribing to events and actions
Your app can listen to all sorts of events and actions — messages being posted, users joining the team, button clicks and more. 

## Events
To listen for events, your app uses the [Events API](https://api.slack.com/events), 
and you will need to subscribe to each one of the events that is relevant for your app.

In order to do that, go to your app configuration page, select the **Event Subscriptions** sidebar. 
You'll be presented with an input box to enter a **Request URL**, which is where Slack sends the events your app is subscribed to. 
For local development, we'll use your ngrok URL from above.

- For example: `https://1234abcde.ngrok.io`

By default Bolt for Python listens for all incoming requests at the `/slack/events` route, so for the Request URL you can enter your ngrok URL appended with `/slack/events`.

- For example: `https://1234abcde.ngrok.io/slack/events`

After you've saved your Request URL, click on **Subscribe to bot events**, then **Add Bot User Event** and search for the event you want to subscribe to. 
Then **Save Changes** using the green button on the bottom right, and your app will start receiving that events as users when they happen.

## Actions
To listen for actions we need to first direct the requests from slack to our server.
The relevant endpoint is the same one as for the events `/slack/events`.
So in order to do that, go to your app configuration page, select the **Interactivity & Shortcuts** sidebar. 
You'll be presented with an input box to enter a **Request URL** similarly to the event one, 
and you should fill it with the same URL (`https://<you-ngrok-link>/slack/events`).


# Responding to events and actions
To respond to events and actions with Bolt for Python, you can write a listener. 
Listeners have access to the event/action body, the entire request payload, and an additional context object that holds helpful information like the bot token you used to instantiate your app.

Let's set up a basic listener to a button click action.
First we will have to create such a button. This could be done with this example code:
```python
import os
from slack_sdk import WebClient

message_with_buttons = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Would you like to drink a happy beer?:beer:",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Yes"
					},
					"action_id": "yes_button",
					"value": "yes"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": ":beers: Of Course!"
					},
					"action_id": "of_course_button",
					"style": "primary",
					"value": "of course"
				}
			]
		}
	]
}

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client.chat_postMessage(channel=some_channel_id, **message_with_buttons)
```

Then paste this listener code, which is using a Python decorator `@app.action("<callback_id>")`, into your existing Bolt app:
```python
@app.action("of_course_button")
def handle_yes_button_click(ack, say):
  ack()
  say("Oh! That's my type of guy :star-struck:")
```
The listener should get as a parameter whatever it needs.
(request, context, options, body, shortcut, action, view, command, event, message, step, say) (read more at Bolt's documentation slack_bolt/kwargs_injection/utils.py)
Ack is a must one so that slack will know that it was handled.

# Slack interactive messages
There are plenty of interactions with shortcuts, modals, or interactive components (such as buttons, select menus, and datepickers).

## Messages builder
Improve your app's design with the [Block Kit Builder](https://app.slack.com/block-kit-builder/). 
This is a prototyping tool that allows you to design Slack apps quickly, 
then paste the code into your Bolt app (Slack also have public [Figma files](https://www.figma.com/@slack) if you'd rather use them to design your app).

## Building with Block Kit
The Block Kit UI framework is built with blocks. Apps can add blocks to surfaces like the Home tab, messages and modals.

Blocks are visual components that can be stacked and arranged to create app layouts. 
Block Kit can make your app's communication clearer while also giving you consistent opportunity to interact with users.

If you are not familiar with the Block Kit UI framework you should get the basics from [this slack guide](https://api.slack.com/block-kit/building).
For the full block elements follow the [slack documentation](https://api.slack.com/reference/block-kit/block-elements).
