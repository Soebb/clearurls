#!/usr/bin/env python3

import logging
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl, User
from unalix import clear_url

from CONFIG import api_hash, api_id, bot_token

logging.basicConfig(format = '[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level = logging.INFO)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token = bot_token)


@bot.on(events.NewMessage(pattern = r'/start'))
async def start_hndlr( event ) :
	await event.reply("""
🧹 I will get you the clear urls without any tracking data using Unalix library.
You can send multiple urls in one message/one inline query as well with newline or space as separator.
❔ How to use?
1. Forward me any message with links, I will reply you with clean URLs
2. Add me to your group, I will reply the messages with clean URLs
3. Use me in inline as well (but limited to 255 chars)
""",
	                  buttons = [Button.url("📝 Source", "https://github.com/GauthamramRavichandran/clearurls")])
	raise events.StopPropagation


@bot.on(events.NewMessage(incoming = True))
async def clearurl_hndlr( event ) :
	if event.message.via_bot is not None :  # Don't handle inline messages
		return
	if event.message.entities :
		to_send = []
		for entity in event.message.entities :
			input_url = None
			if isinstance(entity, MessageEntityTextUrl) :
				print('1 '+entity.url)
			elif isinstance(entity, MessageEntityUrl) :
				print('2 '+event.message.text[entity.offset :entity.offset + entity.length])


@bot.on(events.InlineQuery)
async def handler( event ) :
	builder = event.builder
	input_urls = []
	if '\n' in event.text :
		input_urls.extend(event.text.split('\n'))
	if ' ' in event.text :
		input_urls.extend(event.text.split(' '))
	
	if input_urls :
		result = "\n".join(clear_url(link) for link in input_urls)
	else :
		result = "No URLs found"
	await event.answer([
		builder.article(text = result, link_preview = False)
	])



bot.run_until_disconnected()
