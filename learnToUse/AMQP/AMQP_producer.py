import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'myQueue')

def runChat():
	print 'Introduce text to send. To exit the chat enter a string starting with "!" '
	c = '0'
	while(c != '!'):
		keyboardRead = raw_input()
		c = keyboardRead[0]
		channel.basic_publish(exchange = '', routing_key = 'myQueue', body = keyboardRead)

runChat()
print "Chat closed!"

connection.close()