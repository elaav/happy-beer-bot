import os
from slack_bolt import App

# Initializes the app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Handling the of course button
@app.action("of_course_button")
def handle_yes_button_click(ack, say):
  ack()
  say("Yeah! That's my guy :star-struck:")


# Running the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))