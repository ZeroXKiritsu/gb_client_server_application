import logging
import select
import chat
import jim

logger = logging.getLogger('chat.client')

if __name__ == '__main__':
    logger.debug('App started')

    parser = chat.create_parser()
    namespace = parser.parse_args()

    client_name = input('input name: ')

    sock = chat.get_client_socket(namespace.addr, namespace.port)
    serv_addr = sock.getpeername()
    start_info = f'Connected to server: {serv_addr[0]}:{serv_addr[1]}'
    print(start_info)
    logger.info(start_info)

    jim.PRESENCE['user']['account_name'] = client_name
    try:
        chat.send_data(sock, jim.PRESENCE)
    except ConnectionResetError as e:
        logger.error(e)
        sock.close()
        exit(1)

    while True:
        r_list = []

        try:
            r_list, w_list, e_list = select.select([sock], [], [], 1)
        except Exception as e:
            pass

        if sock in r_list:
            try:
                data = chat.get_data(sock)
            except ConnectionResetError as e:
                logger.error(e)
                break

            if data['response'] != '200':
                logger.debug('App ending')
                break

            if 'messages' in data:
                for message in data['messages']:
                    print(f'{message["time"]} - {message["from"]}: {message["message"]}')

        else:
            msg = input('input message ("exit" for quit): ')
            if msg:
                jim.MESSAGE['message'] = msg

                try:
                    chat.send_data(sock, jim.MESSAGE)
                except ConnectionResetError as e:
                    logger.error(e)
                    break

    sock.close()
