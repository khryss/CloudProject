import pika
import threading

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'serverSend')
channel.queue_declare(queue = 'serverRecv')

def receiveCallBack(ch, method, proprieties, body):
	print body

def consume():
	channel.basic_consume(receiveCallBack, queue = 'serverRecv', no_ack = True)
	channel.start_consuming()
	print 'channel.start_consuming()'

def produce():
	print 'Introduce text to send. To exit the chat enter a string starting with "!" '
	c = '0'
	while(c != '!'):
		keyboardRead = raw_input()
		c = keyboardRead[0]
		channel.basic_publish(exchange = '', routing_key = 'serverSend', body = keyboardRead)
		
consumeThread = threading.Thread(target = consume)
produceThread = threading.Thread(target = produce)

produceThread.start()
consumeThread.start()

produceThread.join()

print "Chat closed!"
connection.close()
