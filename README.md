# Offline Notifier Bot

This is a simple bot I have written to notify me (and others) when one of my other bots goes offline.

## Running

To run the bot you will need a `config.py` file in the root directory.

In this file you will have to specify:
- `BOT_TOKEN`: str - the discord bot token
- `NOTIFICATION_CHANNEL`: int - the channel id for the channel you want notification messages to go to 
- `WEBHOOK_URLS`: [str] - a list of webhook urls which you also want to send a message to when a bot goes online/offline
- `MENTION_USERS`: [int] - a list of discord user ids for the users you want to notify when your bot goes online/offline

To actually launch the bot you just need to run `bot.py`.

## Example bot

In the example-bot directory there is an example of how you might set up a bot which you want to monitor the online/offline status of.
The main code is in `example-bot/cogs/status.py` which sets up a webserver listening on port 5000 which responds simply with status 200 and text "OK" when a request is made to the `/status` endpoint.

To run the example bot you need a `config.py` file in the example-bot directory with:
- `BOT_TOKEN`: str - the discord bot token

This isn't actually required for the cog which runs the webserver though.

## More info

You could also use this basic bot to monitor a website, or other service written in any language if it responds to http requests with a code 200 on the `/status` endpoint.

## Possible Todos?

- Add ability to track uptime of a service
- Easier configurability e.g. notification message content?

