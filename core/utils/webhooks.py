import traceback
from enum import IntEnum

from discordwebhook import Webhook, Embed

from api.settings import settings


class MessageColor(IntEnum):
    GREEN = 3066993
    BLUE = 3447003
    RED = 10038562
    YELLOW = 16705372


def send_webhook(title: str, content: str, color: MessageColor):
    """Send a formatted webhook to discord

    :param str title: title of the message
    :param str content: content of the message, supports markdown
    :param MessageColor color: color code of the strip of the message
    """
    webhook = Webhook(settings.WEBHOOK_URI)
    webhook.username = "Watch Dog"

    embed = Embed(title, content, color=color.value)
    webhook.send_sync("", embed=embed)


def send_errorhook(exception: Exception):
    """Send a webhook to discord that tags the Errors group to alert them of a python code exception. Sends exception
    name and the traceback to facilitate the error finding. Message color is set to RED and is not changeable.

    :param Exception exception: Exception that was raised
    """
    module = exception.__class__.__module__
    if module is None or module == str.__class__.__module__:
        name = exception.__class__.__name__
    else:
        name = module + '.' + exception.__class__.__name__
    webhook = Webhook(settings.WEBHOOK_URI)
    webhook.username = "Watch Dog"

    embed = Embed(name, str(exception), color=MessageColor.RED.value)
    embed.add_field("Traceback", f"```python\n{traceback.format_exc()}```", False)
    webhook.send_sync("<@&963457791262089267>", embed=embed)
