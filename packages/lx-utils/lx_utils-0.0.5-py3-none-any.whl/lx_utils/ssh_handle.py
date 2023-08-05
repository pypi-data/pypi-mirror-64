import paramiko, time, traceback, datetime
from scp import SCPClient


def create_ssh_client(iot_info):
    username, password, host, port = "root", "123456", iot_info['ssh_ip'], iot_info['ssh_port']

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(host, port, username, password)
        log = 'create_ssh_client success {} '.format(iot_info)
        write_log(log)
        return ssh_client

    except Exception as e:
        log = 'create_ssh_client error:{}'.format(e)
        write_log(log)


def upload_file(ssh_client, src_file, des_path):
    '''
    上传文件至网关
    :param ssh_client:
    :param src_file:
    :param des_path:
    :return:
    '''
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=5.0)

    scpclient.put(src_file, des_path)
    log = 'scp file success; src:{}-->des:{}'.format(src_file, des_path)
    write_log(log)


def get_process_running_status(ssh_client, process_name):
    '''
    获取采集网关里的进程运行状态
    :param ssh_client:
    :param process_name:
    :return:
    '''
    cmd = "source /etc/profile; bash /home/root/idi/{}/bin/run.sh status".format(process_name)
    execute_cmd(ssh_client, cmd, wait_time=2)


def restart_process(ssh_client, process_name):
    '''
    重启采集网关里的进程
    :param ssh_client:
    :param process_name:
    :return:
    '''
    cmd = "source /etc/profile; bash /home/root/idi/{}/bin/run.sh restart".format(process_name)
    execute_cmd(ssh_client, cmd, wait_time=5)


def update_site_packages(ssh_client, src_file='../site-packages.tar.gz'):
    '''
    全量更新site_packages.tar.gz
    :param ssh_client:
    :param src_file:
    :return:
    '''
    des_path = "/home/root/armpython/lib/python3.6"
    upload_file(ssh_client, src_file, des_path)

    cmd = "cd /home/root/armpython/lib/python3.6; mv site-packages/ site-packages_back/; tar zxvf site-packages.tar.gz"
    execute_cmd(ssh_client, cmd, wait_time=30)

    restart_process(ssh_client, process_name='idi_iot_0.0.8')
    restart_process(ssh_client, process_name='idi_iot_daemon_0.0.1')


def update_rabbitmq_connector(ssh_client, src_file='../rabbitmq_connector.py'):
    '''
    将mq lib上传至网关并重启采集进程
    :param ssh_client:
    :param src_file:
    :return:
    '''
    des_path = "/home/root/armpython/lib/python3.6/site-packages/mg_app_framework/components/"
    upload_file(ssh_client, src_file, des_path)

    # restart_process(ssh_client, process_name='idi_iot_0.0.8')


def update_rc_local(ssh_client, src_file='S99sztenv'):
    '''
    将开机启动脚本S99sztenv复制到网关，并修改执行权限
    :param ssh_client:
    :param src_file:
    :return:
    '''
    des_path = "/etc/rc5.d/"
    upload_file(ssh_client, src_file, des_path)

    cmd = "source /etc/profile; chmod 777 /etc/rc5.d/S99sztenv".format(des_path)
    execute_cmd(ssh_client, cmd)


def calibrate_iot_time(ssh_client):
    '''
    校准网关时间
    :param ssh_client:
    :return:
    '''
    cmd = 'date -s "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    execute_cmd(ssh_client, cmd)


def execute_cmd(ssh_client, cmd, wait_time=1):
    ssh_session = ssh_client.get_transport().open_session()
    ssh_session.exec_command(cmd)
    print(ssh_session.recv(1024))
    write_log(cmd)
    time.sleep(wait_time)


def write_log(log: str, file_name='update.log'):
    '''
    输出log
    :param log:
    :return:
    '''
    if log:
        print(log)
        file = open(file_name, "a")
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write('{} {}\n'.format(now, log))
        file.close()
