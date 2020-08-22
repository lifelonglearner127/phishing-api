from urllib import parse
from dns import resolver, reversename
from datetime import datetime
from bs4 import BeautifulSoup
from rblwatch import RBLSearch
from .spf import get_spf_record, check_spf
# from .blacklists import google_safebrowsing, phishtank, wot
import re
import pythonwhois
import ipaddress
import requests
import geoip2.database

PATH = 'lib/files/'


def start_url(url):
    """Split URL into: protocol, host, path, params, query and fragment."""
    if not parse.urlparse(url.strip()).scheme:
        url = 'http://' + url
    protocol, host, path, params, query, fragment = parse.urlparse(url.strip())

    result = {
        'url': host + path + params + query + fragment,
        'protocol': protocol,
        'host': host,
        'path': path,
        'params': params,
        'query': query,
        'fragment': fragment
    }
    return result


def count(text, character):
    """Return the amount of certain character in the text."""
    return text.count(character)


def count_vowels(text):
    """Return the number of vowels."""
    vowels = ['a', 'e', 'i', 'o', 'u']
    count = 0
    text_lower = text.lower()
    for i in vowels:
        count += text_lower.count(i)
    return count


def length(text):
    """Return the length of a string."""
    return len(text)


def valid_ip(host):
    """Return if the domain has a valid IP format (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return True
    except Exception:
        return False


def valid_email(text):
    """Return if there is an email in the text."""
    return True if re.findall(r'[\w\.-]+@[\w\.-]+', text) else False


def check_shortener(url):
    """Check if the domain is a shortener."""
    with open(PATH + 'shorteners.txt', 'r') as f:
        for line in f:
            line = line.strip()
            with_www = "www." + line
            host_lower = url['host'].lower()
            if line == host_lower or with_www == host_lower:
                return True
    return False


def check_tld(text):
    """Check for presence of Top-Level Domains (TLD)."""
    with open(PATH + 'tlds.txt', 'r') as f:
        pattern = re.compile("[a-zA-Z0-9.]")
        text_lower = text.lower().strip()
        text_len = len(text)
        for line in f:
            line_len = len(line)
            line = line.strip()
            i = text_lower.find(line)
            while i > -1:
                if ((i + line_len - 1) >= text_len) or not pattern.match(text[i + line_len - 1]):
                    return True
                i = text.find(line, i + 1)
    return False


def count_tld(text):
    """Return amount of Top-Level Domains (TLD) present in the URL."""
    count = 0
    pattern = re.compile("[a-zA-Z0-9.]")
    text_lower = text.lower().strip()
    text_len = len(text)
    with open(PATH + 'tlds.txt', 'r') as f:
        for line in f:
            i = text_lower.find(line.strip())
            line_len = len(line)
            while i > -1:
                if ((i + line_len - 1) >= text_len) or not pattern.match(text[i + line_len - 1]):
                    count += 1
                i = text.find(line.strip(), i + 1)
    return count


def count_params(text):
    """Return number of parameters."""
    return len(parse.parse_qs(text))


def check_word_server_client(text):
    """Return whether the "server" or "client" keywords exist in the domain."""
    text_lower = text.lower()
    return "server" in text_lower or "client" in text_lower


def count_ips(url):
    """Return the number of resolved IPs (IPv4)."""
    if valid_ip(url['host']):
        return 1

    try:
        answers = resolver.query(url['host'], 'A')
        return len(answers)
    except Exception:
        return 0


def count_name_servers(url):
    """Return number of NameServers (NS) resolved."""
    count = 0
    if count_ips(url):
        try:
            answers = resolver.query(url['host'], 'NS')
            return len(answers)
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            split_host = url['host'].split('.')
            while len(split_host) > 0:
                split_host.pop(0)
                supposed_domain = '.'.join(split_host)
                try:
                    answers = resolver.query(supposed_domain, 'NS')
                    count = len(answers)
                    break
                except Exception:
                    count = 0
        except Exception:
            count = 0
    return count


def count_mx_servers(url):
    """Return Number of Resolved MX Servers."""
    count = 0
    if count_ips(url):
        try:
            answers = resolver.query(url['host'], 'MX')
            return len(answers)
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            split_host = url['host'].split('.')
            while len(split_host) > 0:
                split_host.pop(0)
                supposed_domain = '.'.join(split_host)
                try:
                    answers = resolver.query(supposed_domain, 'MX')
                    count = len(answers)
                    break
                except Exception:
                    count = 0
        except Exception:
            count = 0
    return count


def extract_ttl(url):
    """Return Time-to-live (TTL) value associated with hostname."""
    try:
        ttl = resolver.query(url['host']).rrset.ttl
        return ttl
    except Exception:
        return 0


def time_activation_domain(url):
    """Return time (in days) of domain activation."""
    if url['host'].startswith("www."):
        url['host'] = url['host'][4:]

    pythonwhois.net.socket.setdefaulttimeout(3.0)
    try:
        result_whois = pythonwhois.get_whois(url['host'].lower())
        if not result_whois:
            return 0
        creation_date = str(result_whois['creation_date'][0])
        formated_date = " ".join(creation_date.split()[:1])
        d1 = datetime.strptime(formated_date, "%Y-%m-%d")
        d2 = datetime.now()
        return abs((d2 - d1).days)
    except Exception:
        return 0


def expiration_date_register(url):
    """Retorna time (in days) for register expiration."""
    if url['host'].startswith("www."):
        url['host'] = url['host'][4:]

    pythonwhois.net.socket.setdefaulttimeout(3.0)
    try:
        result_whois = pythonwhois.get_whois(url['host'].lower())
        if not result_whois:
            return 0
        expiration_date = str(result_whois['expiration_date'][0])
        formated_date = " ".join(expiration_date.split()[:1])
        d1 = datetime.strptime(formated_date, "%Y-%m-%d")
        d2 = datetime.now()
        return abs((d1 - d2).days)
    except Exception:
        return 0


def extract_extension(text):
    """Return file extension name."""
    pattern = re.compile("[a-zA-Z0-9.]")
    text_lower = text.lower().strip()
    len_text = len(text)
    with open(PATH + 'extensions.txt', 'r') as f:
        for extension in f:
            i = text_lower.find(extension.strip())
            len_extension = len(extension)
            while i > -1:
                if ((i + len_extension - 1) >= len_text) or not pattern.match(text[i + len_extension - 1]):
                    return extension.rstrip().split('.')[-1]
                i = text.find(extension.strip(), i + 1)
    return 'nan'


def check_ssl(url):
    """Check if the ssl certificate is valid."""
    try:
        requests.get(url, verify=True, timeout=3)
        return True
    except Exception:
        return False


def count_redirects(url):
    """Return the number of redirects in a URL."""
    try:
        response = requests.get(url, timeout=3)
        if response.history:
            return len(response.history)
        else:
            return 0
    except Exception:
        return 0


def get_asn_number(url):
    """Return the ANS number associated with the IP."""
    try:
        with geoip2.database.Reader(PATH + 'GeoLite2-ASN.mmdb') as reader:
            if valid_ip(url['host']):
                ip = url['host']
            else:
                ip = resolver.query(url['host'], 'A')
                ip = ip[0].to_text()

            if ip:
                response = reader.asn(ip)
                return response.autonomous_system_number
            else:
                return 0
    except Exception:
        return 0


def get_country(url):
    """Return the country associated with IP."""
    try:
        if valid_ip(url['host']):
            ip = url['host']
        else:
            ip = resolver.query(url['host'], 'A')
            ip = ip[0].to_text()

        if ip:
            reader = geoip2.database.Reader(PATH + 'GeoLite2-Country.mmdb')
            response = reader.country(ip)
            return response.country.iso_code
        else:
            return 'nan'
    except Exception:
        return 'nan'


def get_ptr(url):
    """Return PTR associated with IP."""
    try:
        if valid_ip(url['host']):
            ip = url['host']
        else:
            ip = resolver.query(url['host'], 'A')
            ip = ip[0].to_text()

        if ip:
            r = reversename.from_address(ip)
            result = resolver.query(r, 'PTR')[0].to_text()
            return result
        else:
            return 0
    except Exception:
        return 0


def google_search(url):
    """Check if the url is indexed in google."""
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}

    query = {'q': 'info:' + url}
    google = "https://www.google.com/search?" + parse.urlencode(query)
    try:
        data = requests.get(google, headers=headers, timeout=3)
    except Exception:
        return False
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        (soup.find(id="rso"))
        return True
    except AttributeError:
        return False


def valid_spf(domain):
    """Check if within the registered domain has SPF and if it is valid."""
    spf = get_spf_record(domain)
    if spf:
        return check_spf(spf, domain)
    return False


# def check_blacklists(url):
#     """Check if the URL or Domain is malicious through Google Safebrowsing, Phishtank, and WOT."""
#     if (google_safebrowsing(url) or phishtank(url) or wot(url)):
#         return True
#     return False


# def check_blacklists_ip(url):
#     """Check if the IP is malicious through Google Safebrowsing, Phishtank and WOT."""
#     try:
#         if valid_ip(url['host']):
#             ip = url['host']
#         else:
#             ip = resolver.query(url['host'], 'A')
#             ip = ip[0].to_text()

#         if ip:
#             if (google_safebrowsing(ip) or phishtank(ip) or wot(ip)):
#                 return True
#             return False
#         else:
#             return '?'
#     except Exception:
#         return '?'


def check_rbl(domain):
    """Check domain presence on RBL (Real-time Blackhole List)."""
    searcher = RBLSearch(domain)
    try:
        listed = searcher.listed
    except Exception:
        return False
    for key in listed:
        if key == 'SEARCH_HOST':
            pass
        elif listed[key]['LISTED']:
            return True
    return False


def check_time_response(domain):
    """Return the response time in seconds."""
    try:
        latency = requests.get(
            domain,
            headers={'Cache-Control': 'no-cache'},
            timeout=3
        ).elapsed.total_seconds()
        return latency
    except Exception:
        return 0


def read_file(archive):
    """Read the file with the URLs."""
    with open(archive, 'r') as f:
        urls = ([line.rstrip() for line in f])
        return urls
