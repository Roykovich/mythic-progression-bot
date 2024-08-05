from settings import COMMAND_CHANNEL_ID

async def get_message(bot, message_id, channel_id=COMMAND_CHANNEL_ID):
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    return message
