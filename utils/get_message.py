from settings import COMMAND_CHANNEL_ID

async def get_message(bot, message_id):
    channel = bot.get_channel(COMMAND_CHANNEL_ID)
    message = await channel.fetch_message(message_id)

    return message