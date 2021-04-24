import logging
import os

logger = logging.getLogger('chat.client')

formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(module)-8s - %(message)s')

storage_name = 'log-storage'
if not os.path.exists(storage_name):
    os.mkdir(storage_name)
file_name = os.path.join(storage_name, 'chat.client.log')

file_handler = logging.FileHandler(file_name, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Test launch of logging')