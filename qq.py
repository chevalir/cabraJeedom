import threading
from queue import Queue
import time
import json
import logging
import paho.mqtt.client as paho
logger = logging.getLogger("duibridge")

queues = {}
exitFlag = 0

class mqtt_bridge:
  ## constructor
  def __init__(self, bridgeID, sbNode, source, messageFunc):
    self.client = paho.Client(bridgeID)
    self.broker="broker.mqttdashboard.com"
    self.broker="test.mosquitto.org"
    self.base_topic ="duitest/"+sbNode+"/"
    logger.debug("connecting to broker: " + self.broker)
    self.client.connect(self.broker) 
    self.pub_topic = self.base_topic+"to"+source
    self.sub_topic = self.base_topic+"from"+source
    logger.info("subscribing: "+ self.sub_topic)
    self.client.on_message=messageFunc
    self.client.subscribe(self.sub_topic)
    self.client.publish(self.pub_topic, "init")
    self.client.loop_start() #start loop to process received messages

  def publish_message(self, topic, mess ):
    logger.info('publish on '+topic+ " = "+mess)
    self.client.publish(topic, mess) 

  def send(self,  mess ):
    self.publish_message(self.pub_topic, mess) 

  def subscribe_topic(self, topic):
    logger.debug("subscribing: "+ topic)
    self.client.subscribe(topic)

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, lQueue, lSender):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.tqueue = lQueue
      self.ttsender = lSender 
            
   def run(self):
      print ("Starting " + self.name)
      # print_time(self.name, self.counter, 5)
      msg=0
      while msg != -1:
        msg = self.tqueue.get()
        self.do_work(msg)
        self.tqueue.task_done()
      print ("Exiting " + self.name)

   def do_work(self, count):
   	   print ("Work " + self.name +" :"+str(count))
   	   self.ttsender.send(self.name +" :"+str(count))
   	   #print_time(self.name, self.counter,  count)
        
def print_time(threadName, delay, counter):
   for i in range(counter):
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

def on_message(client, userdata, message):
	line = str(message.payload.decode("utf-8"))
	logger.info("on_message")
	logger.info(line)
	items = line.split("=")
	q = queues.get(int(items[0]))
	logger.info(items)
	logger.info(q)
	q.put(line)

def main():
	# Create new threads
	logger.setLevel("DEBUG")
	console = logging.StreamHandler()
	logger.addHandler(console)
	comArduino = mqtt_bridge("abridgeID", "abridge", "arduino", on_message )
	tq1= Queue()
	queues.update({1:tq1})
	tq2= Queue()
	queues.update({2:tq2})
	thread1 = myThread(1, "Thread-1", 5, tq1, comArduino)
	thread2 = myThread(2, "Thread-2", 4, tq2, comArduino)
	
	# Start new Threads
	thread1.start()
	thread2.start()
	tq1.put(2)
	tq2.put(3)	
	thread1.join()
	thread2.join()
	

if __name__== "__main__":
  main()
