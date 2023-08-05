import telnetlib, socket


async def is_port_open(ip, port) -> bool:
    is_open = False
    try:
        tn = telnetlib.Telnet(ip, port, timeout=2)
        is_open = True
        tn.close()
    except:
        pass

    return is_open


def get_local_host_ip(remote_ip=None) -> str:
    '''
    通过scoket建立UDP连接，getsockname返回连接的ip和port。连接建立失败时connect报错，同时也无法拿到ip和port
    SOCK_STREAM:TCP
    SOCK_DGRAM:UDP
    :return:
    '''
    remote_ip = remote_ip if remote_ip else '8.8.8.8'
    ip = '127.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((remote_ip, 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        pass

    return ip
