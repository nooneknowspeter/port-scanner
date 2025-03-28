import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    for port in range(port_range[0], port_range[-1] + 1):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(0.2)

        try:
            connection = server_socket.connect_ex((target, port))

            if connection == 0:
                open_ports.append(port)
        except socket.gaierror:
            if target[0].isalpha():
                return "Error: Invalid hostname"
            return "Error: Invalid IP address"

        server_socket.close()

    if not verbose:
        return open_ports

    # verbose information example
    """
    Open ports for {URL} ({IP address})
    PORT     SERVICE
    {port}   {service name}
    {port}   {service name}
    """

    verbose_information = ""

    if target[0].isalpha():
        try:
            ip_address = socket.gethostbyname(target)
        except socket.herror:
            raise socket.SO_ERROR

        title = f"Open ports for {target} ({ip_address})\n"
        verbose_information += title
    else:
        ip_address = target
        try:
            target = socket.gethostbyaddr(ip_address)

            title = f"Open ports for {target} ({ip_address})\n"
        except socket.herror:
            title = f"Open ports for {ip_address}\n"

        verbose_information += title

    heading = "PORT     SERVICE\n"
    verbose_information += heading

    for port in open_ports:
        port_information = f"{port:<9}{ports_and_services[port]}\n"
        verbose_information += port_information

    return verbose_information.strip()
