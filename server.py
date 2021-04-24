import logging
import chat
import jim
import server_log_config

client_name = ''

logger = logging.getLogger('chat.server')

if __name__ == '__main__':
    logger.debug('App started')

    parser = chat.create_parser()
    namespace = parser.parse_args()

    sock = chat.get_server_socket(namespace.addr, namespace.port)

    serv_addr = sock.getsockname()
    start_info = f'Server started at {serv_addr[0]}:{serv_addr[1]}'
    print(start_info)
    logger.info(start_info)

    client, address = sock.accept()
    client_info = f'Client connected from {address[0]}:{address[1]}'
    print(client_info)
    logger.info(client_info)

    while True:

        try:
            data_in = chat.get_data(client)
            logger.info(f'Data received from {address} : {data_in}')
        except ConnectionResetError as e:
            logger.error(e)
            break

        if client_name == '':
            if data_in['action'] == 'presence' and data_in['user']['account_name'] != '':
                client_name = data_in['user']['account_name']
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[0]
                print(f'{data_in["time"]} - {data_in["user"]["account_name"]}: {data_in["user"]["status"]}')
            else:
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[1]

        if client_name != '' and data_in['action'] == 'msg':
            print(f'{data_in["time"]} - {client_name}: {data_in["message"]}')
            jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[0]

            if data_in["message"] == 'exit':
                jim.RESPONSE['response'], jim.RESPONSE['alert'] = jim.SERV_RESP[2]

        data_out = jim.RESPONSE

        try:
            chat.send_data(client, data_out)
            logger.info(f'Data sended to {address} : {data_out}')
        except ConnectionResetError as e:
            logger.error(e)
            break

        if data_out['response'] != '200':
            client.close()
            break

    logger.debug('App ending')

    sock.close()
