#!/usr/bin/python
# -*- coding: utf-8 -*-

from pika.adapters import SelectConnection

class RockLoadNode(object):
    def __init__(self, queue='tests'):
        self.channel = None
        self.queue = queue

    def on_connected(self, connection):
        """Called when we are fully connected to RabbitMQ"""
        connection.channel(self.on_channel_open)

    def on_channel_open(self, new_channel):
        """Called when our channel has opened"""
        self.channel = new_channel
        self.channel.queue_declare(queue=self.queue, durable=True, exclusive=False, auto_delete=False, callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
        self.channel.basic_consume(self.handle_delivery, queue=self.queue)

    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ"""
        print body

    def connect(self):
        self.connection = SelectConnection(None, self.on_connected)

        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()

if __name__ == '__main__':
    node = RockLoadNode()
    node.connect()
