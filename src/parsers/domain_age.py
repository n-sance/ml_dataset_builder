import whois
import datetime


def get_domain_age(domain: str) -> int:
    try:
        whois_info = whois.query(domain)
        creation_date = whois_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        return (datetime.datetime.now() - creation_date).days

    except whois.exceptions.WhoisCommandFailed as error:
        print(f'Failed to retrieve data from whois: {error}')
    except whois.exceptions.WhoisQuotaExceeded as error:
        print(f'Whois quota exceeded: {error}')
    except whois.exceptions.WhoisPrivateRegistry as error:
        print(f'Private registry found: {error}')
    except Exception as error:
        print(f'Unexpected error: {error}')