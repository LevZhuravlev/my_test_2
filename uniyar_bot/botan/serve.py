import logging 
from plumbum import cli
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from botan import Core
from yandex_translate import YandexTranslate
from . chatscript import ChatScript
from .model import VolleyProcessor

log = logging.getLogger(__name__)

class ServeSubcmd(cli.Application):
	def main(self):
		log.info('run serve subcommand')
		
		token = Core.config.telegram.api_token()
		if type(token) is not str:
			log.critical('Can not find "telegram:api_token" in config. Exiting.')
			exit(1)

		self._bot = Bot(token=Core.config.telegram.api_token())
		dp = Dispatcher(self._bot)

		self._processor = VolleyProcessor(
			YandexTranslate(Core.config.yandex_translate.api_key()),
			ChatScript(Core.config.chatscript.host(), Core.config.chatscript.port(), 'botan')
			)

		dp.register_message_handler(self.send_welcome, commands=['start', 'help'])
		dp.register_message_handler(self.everything)

		start_polling(
			dp,
			skip_updates=True,
			# on_startup=self.on_startup,
			# on_shutdown=self.on_shutdown
			)
			
	async def everything(self, message: types.Message):
		await self._bot.send_chat_action(message.chat.id, 'typing')

		volley = self._processor.process(text=message.text, user='dev')

		if not volley.output:
			await self._bot.send_message(message.chat.id, ':-)')
			return

		for part in  VolleyProcessor._smart_split(volley.output, 1024):
			if VolleyProcessor._is_cs_command(volley.input_cs):
				part = '```\n{}\n```'.format(part)
			await self._bot.send_message(message.chat.id, part, parse_mode='Markdown')
		


	async def send_welcome(self, message: types.Message):
		volley = self._processor.process(text=message.text, user='dev')
		if not volley.output:
			return
		await self._bot.send_message(message.chat.id, volley.output)