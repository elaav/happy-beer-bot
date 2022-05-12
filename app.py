import os
from slack_bolt import App

# Initializes the app with your bot token and signing secret

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.action("of_course_button")
def handle_yes_button_click(ack, say):
  ack()
  say("Oh! That's my type of guy :star-struck:")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))