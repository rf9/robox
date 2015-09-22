import json
import logging

from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db.transaction import atomic
import pika
from pika.exceptions import ConnectionClosed

from robox.models import DataFile, BinaryFile

__author__ = 'rf9'

_logger = logging.getLogger(__name__)


def validate_barcode(barcode):
    """
    Validate the barcode against EAN13 format if it is 13 digits long, will just accept anything else.
    :raises ValidationError: if barcode is not valid.
    :param barcode: The barcode to be validated
    """
    if len(barcode) == 13 and barcode.isdigit():
        # EAN13
        total = sum(int(ch) * (1 + 2 * (i & 1)) for i, ch in enumerate(barcode[:-1]))
        checksum = (10 - total) % 10
        if str(checksum) != barcode[-1]:
            raise ValidationError("Invalid barcode")


@atomic
def upload_files(barcode, files):
    """
    Atomically uploads a file to the database and parses it.
    :param barcode: The barcode for the file to be uploaded to.
    :param files: The Django files to be uploaded
    :return: The database model of the uploaded file.
    """
    database_files = []

    for file in files:
        try:
            database_file = DataFile.objects.create(
                binary_file=BinaryFile.objects.create(data=file.read(), name=str(file)),
                barcode=barcode,
            )
            database_file.parse()
            database_files.append(database_file)
        except DatabaseError as err:
            try:
                # noinspection PyUnboundLocalVariable
                database_file.binary_file.delete()
            except NameError:
                pass
            raise err

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="upload_notifier")

        channel.basic_publish(exchange='',
                              routing_key='upload_notifier',
                              body=json.dumps({"barcode": barcode, "file_count": len(database_files)}))

        connection.close()
        _logger.debug("Sent message to message queue.")
    except ConnectionClosed:
        _logger.warning("rabbitmq server not responding.")

    return database_files
