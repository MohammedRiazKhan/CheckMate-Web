import socket

def check_if_port_open(host, port):
    # create a socket to make the connection to the instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set a time p
    s.settimeout(1)
    try:
        # connect to the host and port
        s.connect((host, port))
        # if it connected successfully, it will shutdown the connection
        # knowing if it can connect is enough for the telnet
        s.shutdown(socket.SHUT_RDWR)
        # return a status code 1 = Open, 0 = Closed
        return 1, "Connected Successfully to port " + str(port) + "!"
    except socket.error:
        # When an error is encountered, it is assumed it can't connect
        # status code of 0 is returned
        return 0, "Failed to Connect to port " + str(port) + " :("
    finally:
        # close the socket.
        s.close()


print(check_if_port_open('checkmate-mysql.czrub0mfxuvk.eu-west-2.rds.amazonaws.com', 3306))
