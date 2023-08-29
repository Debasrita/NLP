# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:01:12 2022

@author: Codelogic
"""
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
import time
time.clock=time.time
chatbot=ChatBot(name='WattsOn',
                logic_adapters = [{'import_path': 'chatterbot.logic.BestMatch',
                     'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                     'maximum_similarity_threshold': 0.90}],
                preprocessors=['chatterbot.preprocessors.clean_whitespace','chatterbot.preprocessors.unescape_html','chatterbot.preprocessors.convert_to_ascii'])
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')
'''
trainer = ListTrainer(chatbot)
trainer.train(['Hello',
               'Good day. How may I assist you?',
               'What is your name?',
               'I am WattsOn.',
               'Who are you?',
               'I am your friend WattsOn.'])
trainer.train(['Hi',
               'Good day. How may I assist you?'])
trainer.train(['Greetings',
               'Good day. How may I assist you?'])
trainer.train(['What can you do?',
               'I can tell you the weather.'])
trainer.train(['What is the weather today?',
               '**Good day. How may I assist you?'])
trainer.train(['Hi',
               'Good day. How may I assist you?'])
'''
exit_conditions = (":q","end", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🪴 {chatbot.get_response(query)}")