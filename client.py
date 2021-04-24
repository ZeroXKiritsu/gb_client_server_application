import logging
import chat
import jim
import client_log_config

logger = logging.getLogger('chat.client')

if __name__ == '__main__':
    logger.debug('App started')
    client_name = input('input name: ')

    parser = chat.create_parser()
    namespace = parser.parse_args()

    sock = chat.get_client_socket(namespace.addr, namespace.port)

    serv_addr = sock.getpeername()
    start_info = f'Connected to server: {serv_addr[0]}:{serv_addr[1]}'
    print(start_info)
    logger.info(start_info)

    jim.PRESENCE['user']['account_name'] = client_name
    try:
        chat.send_data(sock, jim.PRESENCE)
        logger.info(f'Presence sended to {serv_addr} : {jim.PRESENCE}')
    except ConnectionResetError as e:
        logger.error(e)
        sock.close()
        exit(1)

    while True:
        try:
            data = chat.get_data(sock)
            logger.info(f'Data received from {serv_addr} : {data}')
        except ConnectionResetError as e:
            logger.error(e)
            break

        if data['response'] != '200':
            break

        msg = input('input message ("exit" for quit): ')
        jim.MESSAGE['message'] = msg

        try:
            chat.send_data(sock, jim.MESSAGE)
            logger.info(f'Data sended to {serv_addr} : {jim.MESSAGE}')
        except ConnectionResetError as e:
            logger.error(e)
            break

    logger.debug('App ending')

    sock.close()