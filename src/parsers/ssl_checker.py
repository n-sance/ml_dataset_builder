import ssl
import socket
from datetime import datetime
from ssl import SSLCertVerificationError


def check_ssl_certificate(url: str, scheme: str = '') -> (bool, bool, datetime):
    """
    Checks if SSL cert exists for a given URL
    :param url:
    :return: (is certificate exists, is certificate self-signed)
    """
    if scheme == 'http':
        # No need to spend time on socket connection if provided scheme is http
        return False, False, None
    try:
        sock = socket.create_connection((url, 443), timeout=1)
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=url)
        certificate = sock.getpeercert()
        if certificate:
            date = datetime.strptime(certificate['notBefore'], "%b %d %H:%M:%S %Y %Z")
        else:
            date = None

        is_self_signed = certificate['issuer'] == certificate['subject'] if certificate else None

        return bool(sock.getpeercert()), is_self_signed, date

    except SSLCertVerificationError:
        print(f'Self-signed crt for {url}')
        return True, True, None
    except socket.error as e:
        print("Socket error:", e)
        return '', '', None
    except ssl.CertificateError as e:
        print("Crt error:", e)
        return '', '', None

