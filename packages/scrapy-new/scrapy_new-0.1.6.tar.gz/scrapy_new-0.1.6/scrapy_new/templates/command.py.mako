## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import signal

from scrapy.utils.log import configure_logging
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from sqlalchemy.orm import Session

from helpers import mysql_connection_string
% if use_rabbit:
from helpers import PikaBlockingConnection
% endif
from .base_command import BaseCommand


class ${class_name}(BaseCommand):
    def __init__(self):
        super().__init__()
        self.engine = None
        self.session = None
        % if use_rabbit:
        self.connection = None
        self.channel = None
        % endif
        self.stopped = False

    def connect(self):
        """Connects to database and rabbitmq (optionally)"""
        self.engine = create_engine(mysql_connection_string())
        self.session = Session(self.engine)
        % if use_rabbit:

        queue_name = self.settings.get("QUEUE_NAME")  # LINKS_QUEUE or SAVER_QUEUE
        rabbitmq = PikaBlockingConnection(queue_name, self.settings)
        self.connection = rabbitmq.rabbit_connection
        self.channel = rabbitmq.rabbit_channel
        self.channel.queue_declare(queue=queue_name, durable=True)
        % endif

    def signal_handler(self, signal, frame):
        self.logger.info("received signal, exiting...")
        self.stopped = True

    def add_options(self, parser):
        super().add_options(parser)

    def run(self, args, opts):
        self.set_logger("${logger_name}", self.settings.get("LOG_LEVEL"))
        configure_logging()
        self.connect()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # your code here

        % if use_rabbit:
        self.channel.close()
        self.connection.close()
        % endif
        self.session.close()
