import posixpath
import csv
from lib import functions_v2 as f


LANG_MAP = {
    'asp': 0,
    'aspx': 1,
    'cfm': 2,
    'cgi': 3,
    'com': 4,
    'css': 5,
    'doc': 6,
    'gif': 7,
    'htm': 8,
    'html': 9,
    'jpg': 10,
    'jsp': 11,
    'php': 12,
    'pl': 13,
    'png': 14,
    'svg': 15,
    'swf': 16,
    'torrent': 17,
    'txt': 18,
    'xhtml': 19,
    'js': 20,
    'exe': 21,
    'dll': 22,
    'zip': 23,
    'jar': 24,
    'bin': 25,
    'nan': 26,
}
COUNTRY_MAP = {
    'AE': 0,
    'AR': 1,
    'AT': 2,
    'AU': 3,
    'BD': 4,
    'BE': 5,
    'BG': 6,
    'BR': 7,
    'BY': 8,
    'CA': 9,
    'CH': 10,
    'CL': 11,
    'CN': 12,
    'CO': 13,
    'CY': 14,
    'CZ': 15,
    'DE': 16,
    'DK': 17,
    'DO': 18,
    'DZ': 19,
    'EE': 20,
    'ES': 21,
    'FI': 22,
    'FR': 23,
    'GB': 24,
    'GE': 25,
    'GM': 26,
    'GR': 27,
    'HK': 28,
    'HR': 29,
    'HU': 30,
    'ID': 31,
    'IE': 32,
    'IL': 33,
    'IN': 34,
    'IR': 35,
    'IS': 36,
    'IT': 37,
    'JP': 38,
    'KE': 39,
    'KH': 40,
    'KR': 41,
    'KY': 42,
    'KZ': 43,
    'LT': 44,
    'LU': 45,
    'LV': 46,
    'MA': 47,
    'MK': 48,
    'MN': 49,
    'MU': 50,
    'MX': 51,
    'MY': 52,
    'NG': 53,
    'NL': 54,
    'NO': 55,
    'NZ': 56,
    'NA': 57,
    'PA': 58,
    'PE': 59,
    'PL': 60,
    'PT': 61,
    'RO': 62,
    'RS': 63,
    'RU': 64,
    'SE': 65,
    'SG': 66,
    'SI': 67,
    'SK': 68,
    'TH': 69,
    'TR': 70,
    'TW': 71,
    'TZ': 72,
    'UA': 73,
    'US': 74,
    'VG': 75,
    'VN': 76,
    'ZA': 77,
    'ZW': 78,
    'nan': 79,
    'None': 80
}


def attributes():
    """Output file attributes."""
    list_attributes = [
        'dot_url', 'hyphe_url', 'underline_url', 'bar_url', 'question_url',
        'equal_url', 'arroba_url', 'ampersand_url', 'exclamation_url',
        'til_url', 'comma_url', 'plus_url', 'asterisk_url', 'hashtag_url',
        'money_sign_url', 'percentage_url', 'count_tld_url', 'len_url',
        'dot_host', 'hyphe_host', 'underline_host', 'arroba_host',
        'vowels_host', 'len_host', 'ip_exist', 'server_client',
        'dot_path', 'hyphe_path', 'underline_path', 'bar_path', 'equal_path',
        'arroba_path', 'ampersand_path', 'exclamation_path', 'til_path',
        'comma_path', 'plus_path', 'asterisk_path', 'money_sign_path',
        'percentage_path', 'len_path', 'dot_file', 'hyphe_file',
        'underline_file', 'equal_file', 'arroba_file', 'ampersand_file',
        'exclamation_file', 'til_file', 'comma_file', 'plus_file',
        'asterisk_file', 'hashtag_file', 'money_sign_file', 'percentage_file',
        'len_file', 'dot_params', 'hyphe_params', 'underline_params',
        'bar_params', 'question_params', 'equal_params', 'arroba_params',
        'ampersand_params', 'exclamation_params', 'til_params', 'comma_params',
        'plus_params', 'asterisk_params', 'hashtag_params',
        'money_sign_params', 'percentage_params', 'len_params', 'tld_params',
        'number_params', 'email_exist', 'extension', 'rbl', 'time_domain',
        'spf', 'country', 'activation_time', 'expiration_time', 'count_ip',
        'count_ns', 'count_mx', 'ttl', 'ssl', 'count_redirect',
        'google_url', 'google_domain', 'phishing'
    ]
    return list_attributes


def extract_features(url):
    dict_url = f.start_url(url)
    """LEXICAL"""
    # URL
    url = dict_url['url']
    dot_url = url.count('.')
    hyphe_url = url.count('-')
    underline_url = url.count('_')
    bar_url = url.count('/')
    question_url = url.count('?')
    equal_url = url.count('=')
    arroba_url = url.count('@')
    ampersand_url = url.count('&')
    exclamation_url = url.count('!')
    til_url = url.count('~')
    comma_url = url.count(',')
    plus_url = url.count('+')
    asterisk_url = url.count('*')
    hashtag_url = url.count('#')
    money_sign_url = url.count('$')
    percentage_url = url.count('%')
    len_url = len(url)
    email_exist = f.valid_email(url)
    count_tld_url = f.count_tld(url)

    # DOMAIN
    host = dict_url['host']
    dot_host = host.count('.')
    hyphe_host = host.count('-')
    underline_host = host.count('_')
    arroba_host = host.count('@')
    vowels_host = f.count_vowels(host)
    len_host = len(host)
    ip_exist = f.valid_ip(host)
    server_client = f.check_word_server_client(host)

    # DIRECTORY
    if dict_url['path']:
        path = dict_url['path']
        dot_path = path.count('.')
        hyphe_path = path.count('-')
        underline_path = path.count('_')
        bar_path = path.count('/')
        equal_path = path.count('=')
        arroba_path = path.count('@')
        ampersand_path = path.count('&')
        exclamation_path = path.count('!')
        til_path = path.count('~')
        comma_path = path.count(',')
        plus_path = path.count('+')
        asterisk_path = path.count('*')
        money_sign_path = path.count('$')
        percentage_path = path.count('%')
        len_path = len(path)

        # FILE
        path_basename = posixpath.basename(path)
        dot_file = path_basename.count('.')
        hyphe_file = path_basename.count('-')
        underline_file = path_basename.count('_')
        equal_file = path_basename.count('=')
        arroba_file = path_basename.count('@')
        ampersand_file = path_basename.count('&')
        exclamation_file = path_basename.count('!')
        til_file = path_basename.count('~')
        comma_file = path_basename.count(',')
        plus_file = path_basename.count('+')
        asterisk_file = path_basename.count('*')
        hashtag_file = path_basename.count('#')
        money_sign_file = path_basename.count('$')
        percentage_file = path_basename.count('%')
        len_file = len(path_basename)
        extension = LANG_MAP[f.extract_extension(path_basename)]
    else:
        dot_path = 0
        hyphe_path = 0
        underline_path = 0
        bar_path = 0
        equal_path = 0
        arroba_path = 0
        ampersand_path = 0
        exclamation_path = 0
        til_path = 0
        comma_path = 0
        plus_path = 0
        asterisk_path = 0
        money_sign_path = 0
        percentage_path = 0
        len_path = 0

        # FILE
        dot_file = 0
        hyphe_file = 0
        underline_file = 0
        equal_file = 0
        arroba_file = 0
        ampersand_file = 0
        exclamation_file = 0
        til_file = 0
        comma_file = 0
        plus_file = 0
        asterisk_file = 0
        hashtag_file = 0
        money_sign_file = 0
        percentage_file = 0
        len_file = 0
        extension = LANG_MAP['nan']

    # PARAMETERS
    if dict_url['query']:
        query = dict_url['query']
        dot_params = query.count('.')
        hyphe_params = query.count('-')
        underline_params = query.count('_')
        bar_params = query.count('/')
        question_params = query.count('?')
        equal_params = query.count('=')
        arroba_params = query.count('@')
        ampersand_params = query.count('&')
        exclamation_params = query.count('!')
        til_params = query.count('~')
        comma_params = query.count(',')
        plus_params = query.count('+')
        asterisk_params = query.count('*')
        hashtag_params = query.count('#')
        money_sign_params = query.count('$')
        percentage_params = query.count('%')
        len_params = len(query)
        tld_params = f.check_tld(query)
        number_params = f.count_params(query)
    else:
        dot_params = 0
        hyphe_params = 0
        underline_params = 0
        bar_params = 0
        question_params = 0
        equal_params = 0
        arroba_params = 0
        ampersand_params = 0
        exclamation_params = 0
        til_params = 0
        comma_params = 0
        plus_params = 0
        asterisk_params = 0
        hashtag_params = 0
        money_sign_params = 0
        percentage_params = 0
        len_params = 0
        tld_params = 0
        number_params = 0

    """BLACKLIST"""

    """HOST"""
    spf = f.valid_spf(host)
    rbl = f.check_rbl(host)
    time_domain = f.check_time_response(
        f"{dict_url['protocol']}://{dict_url['host']}")
    country = COUNTRY_MAP[f.get_country(dict_url)]
    activation_time = f.time_activation_domain(dict_url)
    expiration_time = f.expiration_date_register(dict_url)
    count_ip = f.count_ips(dict_url)
    count_ns = f.count_name_servers(dict_url)
    count_mx = f.count_mx_servers(dict_url)
    ttl = f.extract_ttl(dict_url)

    """OTHERS"""
    ssl = f.check_ssl('https://' + dict_url['url'])
    count_redirect = f.count_redirects(
        dict_url['protocol'] + '://' + dict_url['url'])
    google_url = 0
    google_domain = 0

    result = [
        dot_url, hyphe_url, underline_url, bar_url, question_url,
        equal_url, arroba_url, ampersand_url, exclamation_url,
        til_url, comma_url, plus_url, asterisk_url, hashtag_url,
        money_sign_url, percentage_url, count_tld_url, len_url,
        dot_host, hyphe_host, underline_host, arroba_host,
        vowels_host, len_host, ip_exist, server_client,
        dot_path, hyphe_path, underline_path, bar_path, equal_path,
        arroba_path, ampersand_path, exclamation_path, til_path,
        comma_path, plus_path, asterisk_path, money_sign_path,
        percentage_path, len_path, dot_file, hyphe_file,
        underline_file, equal_file, arroba_file, ampersand_file,
        exclamation_file, til_file, comma_file, plus_file,
        asterisk_file, hashtag_file, money_sign_file, percentage_file,
        len_file, dot_params, hyphe_params, underline_params,
        bar_params, question_params, equal_params, arroba_params,
        ampersand_params, exclamation_params, til_params, comma_params,
        plus_params, asterisk_params, hashtag_params,
        money_sign_params, percentage_params, len_params, tld_params,
        number_params, email_exist, extension, rbl, time_domain,
        spf, country, activation_time, expiration_time, count_ip,
        count_ns, count_mx, ttl, ssl, count_redirect,
        google_url, google_domain,
    ]

    for n, i in enumerate(result):
        if i is True:
            result[n] = 1
        elif i is False:
            result[n] = 0
        else:
            result[n] = float(result[n])
    return result


def main(urls, dataset, phishing):
    with open(dataset, "w") as output:
        writer = csv.writer(output)
        writer.writerow(attributes())
        for url in f.read_file(urls):
            print(f"extracting feature from {url}...")
            result = extract_features(url)
            result.append(phishing)
            writer.writerow(result)
            print(f"extracted features from {url}...")


if __name__ == "__main__":
    from datetime import datetime
    before = datetime.now()
    print(before)
    extract_features("kalantzis.net")
    after = datetime.now()
    print((after-before).total_seconds())
