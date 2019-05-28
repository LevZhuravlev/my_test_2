import pytest
from mock import MagicMock
from botan.model import VolleyProcessor

class TestVolleyProcessor:

    @pytest.mark.parametrize("text, result", 
    [
        ('Привет',  True), 
        ('Hello', False),
        ('Расскажи про beatles, queen', True)
    ])
    def test__is_ru(self, text, result):
        assert VolleyProcessor._is_ru(text) == result
    
    @pytest.mark.parametrize("text, result", 
    [
        ('Привет!',  False), 
        ('Hello', False),
        (':commands', True),
        ('', False),
        (':::::::', True)
    ])
    def test__is_cs_command(self, text, result):
        assert VolleyProcessor._is_cs_command(text) == result

    @pytest.mark.parametrize("user, input, input_cs, output_cs, output, translate_call_count", 
    [
        ('user', 'test', 'test', 'tset', 'тсет', 1), 
        ('user', 'тест', 'test', 'tset', 'тсет', 2),
        ('user', ':commands_1', 'commands_1', '1_sdnammoc', '1_сднаммок', 1),
        ('dev', ':commands_2', ':commands_2', '2_sdnammoc:', '2_sdnammoc:', 0),
        ('dev', ':pos', ':pos', ' ', '', 0)
    ])
    def test_create_translate(self, user, input, input_cs, output_cs, output, translate_call_count):
        translator = MagicMock()
        translator.translate.side_effect = lambda t, lang: { 
                                                            'en':{'text':[input_cs]}, 
                                                            'ru':{'text':[output]} 
                                                            }[lang]

        chatscript = MagicMock()
        chatscript.say.return_value = output_cs
        
        v = VolleyProcessor(translator, chatscript).process(text=input, user=user)

        assert v.input == input
        assert v.input_cs == input_cs
        assert v.output_cs == output_cs
        assert v.output == output
        assert translator.translate.call_count == translate_call_count
        assert chatscript.say.call_count == 1
    

    def test_smart_split(self):
        parts = VolleyProcessor._smart_split('1234\n\n5678', 6)
        assert parts[0] == '1234\n\n'
        assert parts[1] == '5678'

        parts = VolleyProcessor._smart_split('1234\r\n5678', 6)
        assert parts[0] == '1234\r\n'
        assert parts[1] == '5678'

        parts = VolleyProcessor._smart_split('12\n\n34\n\n5678', 8)
        assert parts[0] == '12\n\n34\n\n'
        assert parts[1] == '5678'

        parts = VolleyProcessor._smart_split('12\n3456\n\n78', 6)
        assert parts[0] == '12\n'
        assert parts[1] == '3456\n\n'
        assert parts[2] == '78'

        parts = VolleyProcessor._smart_split('12. 3456\n\n78', 7)
        assert parts[0] == '12.'
        assert parts[1] == ' 3456\n\n'
        assert parts[2] == '78'

        parts = VolleyProcessor._smart_split('12345678', 5)
        assert parts[0] == '12345'
        assert parts[1] == '678'

        parts = VolleyProcessor._smart_split('abcd.\nefghijklm', 4)
        assert parts[0] == 'abcd'
        assert parts[1] == '.\n'
        assert parts[2] == 'efgh'
        assert parts[3] == 'ijkl'
        assert parts[4] == 'm'


