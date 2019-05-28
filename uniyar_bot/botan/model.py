from enum import Enum
import logging
from collections import namedtuple  

log = logging.getLogger(__name__)

Volley = namedtuple('Volley', ['input', 'input_cs', 'output_cs', 'output'])

class VolleyProcessor:
	def __init__(self, translator, chatscript):
		self._translator = translator
		self._chatscript = chatscript
	
	def process(self, text, user):
		input_cs = text if self._is_en(text) else self._translate(text, 'en')

		#TODO нормальная проверка роли пользователя
		if user != 'dev': input_cs = self._sanitize(input_cs)
		
		output_cs = self._ask_chatscript(input_cs)

		if self._is_blank(output_cs):
			return Volley(input=text, input_cs=input_cs, output_cs=output_cs, output='')

		if self._is_en(output_cs) and not self._is_cs_command(input_cs):
			output = self._translate(output_cs, 'ru').replace('\r', '')
		else:
			output = output_cs.replace('\r', '')

		return Volley(input=text, input_cs=input_cs, output_cs=output_cs, output=output)

	
	def _translate(self, text, target='en'):
		log.info('"{}" -> "{}"'.format(text, target))
		result = self._translator.translate(text, target)['text'][0]
		log.info(result)
		return result

	def _ask_chatscript(self, text):
		log.debug('"{}"'.format(text))
		return self._chatscript.say(text)
	
	@staticmethod
	def _smart_split(text, max_size = 2048):
		def _split_keeping_delimeter(text, delimeter):
			result = [chunk+delimeter for chunk in text.split(delimeter)]
			result[-1] = result[-1].strip(delimeter)
			return result

		def _splitter(text, s_func, depth=0):
			print('\t'*depth+'start:'+text.__repr__())
			if len(s_func) == 0:
				return 
			current = s_func[0]
			others = s_func[1:]
			parts = ['']
			for chunk in current(text):
				print('\t'*depth+chunk.__repr__())
				if len(parts[len(parts)-1]+chunk) <= max_size:
					parts[len(parts)-1] += chunk
				elif len(chunk) <= max_size:
					parts.append(chunk)
				else:
					if parts[len(parts)-1]=='':
						parts.remove('')
					parts.extend(_splitter(chunk, others, depth+1))
				print('\t'*depth+'parts:', parts)	
			print('\t'*depth+text.__repr__()+' -> return:', parts)
			return parts

		return _splitter(text, [lambda t:_split_keeping_delimeter(t, '\n\n'), 
								lambda t:_split_keeping_delimeter(t, '\n'),
								lambda t:_split_keeping_delimeter(t, '.'),
								lambda t:_split_keeping_delimeter(t, ' '),
								lambda t:t])

	@staticmethod
	def _is_blank (text):
		return not (text and text.strip())

	@staticmethod
	def _sanitize(text):
		return text.strip(':')
	
	@staticmethod
	def _is_cs_command(text):
		return len(text) > 0 and text[0] == ':'
	
	@staticmethod
	def _is_ru(text):
		en, ru, other = 0, 0, 0

		for c in text.lower():
			if c in 'abcdefghijklmnopqrstuvwxyz':
				en += 1
			elif c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
				ru += 1
			else:
				other += 1
			
		return ru*5 > en #empirical rule
	
	@staticmethod
	def _is_en(text):
		return not VolleyProcessor._is_ru(text)
