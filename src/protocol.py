"""Protocol for chat server - Computação Distribuida Assignment 1."""
import json
import time
import xml.etree.ElementTree as element_tree
import xml
from socket import socket
import pickle

class Message:
    """Message Type."""
    def __init__(self,command):
        self.command=command
        pass

class RegisterMessage(Message):
    """Message to register username in the server."""
    def __init__(self,topic,command="register"):
        super().__init__(command)
        self.topic=topic
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command, 'topic':self.topic,'serializer':1})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command, 'topic':self.topic,'serializer':2})
    def _XMLQueue__str__xml(self):
        msg = {'command':self.command, 'topic':self.topic,'serializer':0}
        conv = ('<?xml version="1.0"?><data command="%(command)s" topic="%(topic)s"  serializer="%(serializer)s"></data>' % msg)
        return conv

class CancelMessage(Message):
    """Message to register username in the server."""
    def __init__(self,topic,command="cancel"):
        super().__init__(command)
        self.topic=topic
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command, 'topic':self.topic})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command, 'topic':self.topic})

class ListMessage(Message):
    """Message to register username in the server."""
    def __init__(self,command="list"):
        super().__init__(command)
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command})
    def _XMLQueue__str__xml(self):
        msg = {'command':self.command}
        conv = ('<?xml version="1.0"?><data command="%(command)s"></data>' % msg)
        return conv

class PushMessage(Message):
    """Message to register username in the server."""
    def __init__(self,topic,value,command="push"):
        super().__init__(command)
        self.topic=topic
        self.value=value
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command,'topic':self.topic,'value':self.value})
    def _Queue__str__json(self):
        return json.dumps({'command':self.command,'topic':self.topic,'value':self.value})
    def PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command,'topic':self.topic,'value':self.value})
    def _Queue__str__pickle(self):
        return pickle.dumps({'command':self.command,'topic':self.topic,'value':self.value})

    def _XMLQueue__str__xml(self):
        msg = {'command':self.command,'topic':self.topic,'value':self.value}
        conv = ('<?xml version="1.0"?><data command="%(command)s" topic="%(topic)s"><value>%(value)s"</value></data>' % msg)
        return conv
    def _Queue__str__xml(self):
        msg = {'command':self.command,'topic':self.topic,'value':self.value}
        conv = ('<?xml version="1.0"?><data command="%(command)s" topic="%(topic)s"><value>%(value)s"</value></data>' % msg)
        return conv


class PullMessage(Message):
    """Message to register username in the server."""
    def __init__(self,topic,command="pull"):
        super().__init__(command)
        self.topic=topic
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command,'topic':self.topic})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command,'topic':self.topic})
    def _XMLQueue__str__xml(self):
        msg = {'command':self.command,'topic':self.topic}
        conv = ('<?xml version="1.0"?><data command="%(command)s" topic="%(topic)s"></data>' % msg)
        return conv


class RepPullMessage(Message):
    """Message to register username in the server."""
    def __init__(self,value,command="reppull"):
        super().__init__(command)
        self.value=value
        
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command,'value':self.value})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command,'value':self.value})
    def _XMLQueue__str__xml(self):
        msg = {'command':self.command,'value':self.value}
        conv = ('<?xml version="1.0"?><data command="%(command)s" value="%(value)s"></data>' % msg)
        return conv

class RepPushMessage(Message):
    """Message to register username in the server."""
    def __init__(self,value,command="reppull"):
        super().__init__(command)
        self.value=value
    def _JSONQueue__str__json(self):
        return json.dumps({'command':self.command,'value':self.value})
    def _PICKLEQueue__str__pickle(self):
        return pickle.dumps({'command':self.command,'value':self.value})
    def _XMLQueue__str__xml(self):
        msg = {'command':self.command,'value':self.value}
        conv = ('<?xml version="1.0"?><data command="%(command)s" value="%(value)s"></data>' % msg)
        return conv

class CDProto:
    """Computação Distribuida Protocol."""

    @classmethod
    def register(cls, topic: str) -> RegisterMessage:
        """Creates a RegisterMessage object."""
        return RegisterMessage(topic)
    @classmethod
    def cancel(cls, topic: str) -> CancelMessage:
        """Creates a RegisterMessage object."""
        return CancelMessage(topic)

    @classmethod
    def lists(cls) -> ListMessage:
        """Creates a RegisterMessage object."""
        return ListMessage()  
          
    @classmethod
    def push(cls, topic: str,value:str) -> PushMessage:
        """Creates a RegisterMessage object."""
        return PushMessage(topic,value)  

    @classmethod
    def pull(cls, topic: str) -> PullMessage:
        """Creates a RegisterMessage object."""
        return PullMessage(topic)   

    @classmethod
    def reppull(cls, value: str) -> RepPullMessage:
        """Creates a RegisterMessage object."""
        return RepPullMessage(value)   
    
    def reppush(cls, value: str) -> RepPushMessage:
        """Creates a RegisterMessage object."""
        return RepPushMessage(value)   
    
    @classmethod
    def send_msg(cls, connection: socket, msg: Message ,serializer:int):
        """Sends through a connection a Message object."""
        data=msg.encode(encoding='UTF-8') #dar encode para bytes
        ser=serializer.to_bytes(2,byteorder='big')
        mess=len(data).to_bytes(2,byteorder='big') #tamanho da mensagem em bytes
        mess+=ser
        mess+=data #mensagem final contendo o cabeçalho e a mensagem
        connection.send(mess) #enviar mensagem final

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        """Receives through a connection a Message object."""
        header=connection.recv(2) #recevemos os 2 primeiros bits
        head=int.from_bytes(header,byteorder='big') #contem o tamanho da mensagem 
        if head!=0:
            ser=connection.recv(2)
            serializer=int.from_bytes(ser,byteorder='big') # vemos o serializer da mensagem
            message=connection.recv(head) #recebemos os bits correspondente á mensagem
            datat=message.decode(encoding='UTF-8')#descodificamos a mensagem 
            if(serializer==1):
                data=json.loads(datat) # vira json
            elif (serializer==2):
                data=pickle.loads(datat) # vira pickle
            else:
                decoded_xml = element_tree.fromstring(datat)
                data = decoded_xml.attrib
            return data
            
        else:
            return None
        

class CDProtoBadFormat(Exception):
    """Exception when source message is not CDProto."""

    def __init__(self, original_msg: bytes=None) :
        """Store original message that triggered exception."""
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        """Retrieve original message as a string."""
        return self._original.decode("utf-8")