from channels.generic.websocket import WebsocketConsumer
import json
import threading
import logging

from queue import Queue

from .board import Board
from .expert import ExpertPlayer

class ChatConsumer(WebsocketConsumer):
    def connect(self):  
        self.accept()
        self.queue = Queue(maxsize=1)  #定义一个queue，作为两个线程的交互数据

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logging.info("{}".format(text_data_json))

        if text_data_json['msgtype'] == 'playinfo':
            start_game_thread = threading.Thread(target=start_game,
                args=(self,text_data_json['player'],text_data_json['whoisfirst']))
            start_game_thread.start()
        elif text_data_json['msgtype'] == 'chess' :
            self.queue.put(text_data_json)  #放入接收的数据


class WebPlayer(object):
    def __init__(self,consumer):
        self.consumer = consumer
        pass

    def get_action(self,board):
        webplayer_data=self.consumer.queue.get()   #
        action = board.location_to_action(webplayer_data['Px'],
                                          webplayer_data['Py'])
        logging.info("action:{}".format(action))
        return action

    def reply(self,end,winner,color,x,y):
        reply_data={}
        reply_data['msgtype'] = 'chess'
        reply_data['Color'] = color
        reply_data['Px'] = x
        reply_data['Py'] = y
        reply_data['end'] = end
        reply_data['winner'] = winner
        self.consumer.send(json.dumps(reply_data))
        logging.info("reply_data:{}".format(reply_data))

def log_config():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename = 'gomoku.log', 
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)

def start_game(consumer,player,whoisfirst):
    log_config()
    logging.info("{},{}".format(player,whoisfirst))

    my_board = Board()
    
    player1 = WebPlayer(consumer)
    player2 = ExpertPlayer()
    if whoisfirst == 'Me':
        my_board.start(player1, player2)
    else:
        my_board.start(player2, player1)

