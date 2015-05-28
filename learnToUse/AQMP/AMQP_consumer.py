import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

channel =  connection.channel()

#channel.declare_channel(queue = "myQueue")

def callback(ch, method, proprieties, body):
	print "Received %r" % (body,)

print 'Wait for messages. Press CTRL+C to exit'

channel.basic_consume(callback, queue = 'myQueue', no_ack = True)

channel.start_consuming()