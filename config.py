import socket

HOST_SPADE_IP = '10.24.20.61'
HOST_NAME = socket.gethostname()

connected = {
    # agent_local_ip source : [[agent_name_destination, spade_platform_ip]]
    'dell': [['lubuntu1_receiver', HOST_SPADE_IP]],
    'lubuntu1': [['lubuntu2_receiver', HOST_SPADE_IP], ['dell_receiver', HOST_SPADE_IP]],
    'lubuntu2': [['dell_receiver', HOST_SPADE_IP]]
}
