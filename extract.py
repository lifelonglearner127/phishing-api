from lib.functions import *
import posixpath
import csv


PRODUCTION_COLUMNS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 25, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 101, 102, 103, 104, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116]
LANG_MAP = {'asp': 0, 'aspx': 1, 'cfm': 2, 'cgi': 3, 'com': 4, 'css': 5, 'doc': 6, 'gif': 7, 'htm': 8, 'html': 9, 'jpg': 10, 'jsp': 11, 'php': 12, 'pl': 13, 'png': 14, 'svg': 15, 'swf': 16, 'torrent': 17, 'txt': 18, 'xhtml': 19, 'nan': 20}
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
    list_attributes = ['dot_url', 'hyphe_url', 'underline_url', 'bar_url', 'question_url', 'equal_url', 'arroba_url', 'ampersand_url', 'exclamation_url', 'til_url', 'comma_url', 'plus_url', 'asterisk_url', 'hashtag_url', 'money_sign_url', 'percentage_url', 'count_tld_url', 'len_url', 'dot_host', 'hyphe_host', 'underline_host', 'arroba_host', 'vowels_host', 'len_host', 'ip_exist', 'server_client', 'dot_path', 'hyphe_path', 'underline_path', 'bar_path', 'equal_path', 'arroba_path', 'ampersand_path', 'exclamation_path', 'til_path', 'comma_path', 'plus_path', 'asterisk_path', 'money_sign_path', 'percentage_path', 'len_path', 'dot_file', 'hyphe_file', 'underline_file', 'equal_file', 'arroba_file', 'ampersand_file', 'exclamation_file', 'til_file', 'comma_file', 'plus_file', 'asterisk_file', 'hashtag_file', 'money_sign_file', 'percentage_file', 'len_file', 'dot_params', 'hyphe_params', 'underline_params', 'bar_params', 'question_params', 'equal_params', 'arroba_params', 'ampersand_params', 'exclamation_params', 'til_params', 'comma_params', 'plus_params', 'asterisk_params', 'hashtag_params', 'money_sign_params', 'percentage_params', 'len_params', 'tld_params', 'number_params', 'email_exist', 'extension', 'rbl', 'time_domain', 'spf', 'country', 'activation_time', 'expiration_time', 'count_ip', 'count_ns', 'count_mx', 'ttl', 'ssl', 'count_redirect', 'google_url', 'google_domain','phishing']
    return list_attributes


def extract_features(url):
    dict_url = start_url(url)
    """LEXICAL"""
    # URL
    dot_url = str(count(dict_url['url'], '.'))
    hyphe_url = str(count(dict_url['url'], '-'))
    underline_url = str(count(dict_url['url'], '_'))
    bar_url = str(count(dict_url['url'], '/'))
    question_url = str(count(dict_url['url'], '?'))
    equal_url = str(count(dict_url['url'], '='))
    arroba_url = str(count(dict_url['url'], '@'))
    ampersand_url = str(count(dict_url['url'], '&'))
    exclamation_url = str(count(dict_url['url'], '!'))
    blank_url = str(count(dict_url['url'], ' '))
    til_url = str(count(dict_url['url'], '~'))
    comma_url = str(count(dict_url['url'], ','))
    plus_url = str(count(dict_url['url'], '+'))
    asterisk_url = str(count(dict_url['url'], '*'))
    hashtag_url = str(count(dict_url['url'], '#'))
    money_sign_url = str(count(dict_url['url'], '$'))
    percentage_url = str(count(dict_url['url'], '%'))
    len_url = str(length(dict_url['url']))
    email_exist = str(valid_email(dict_url['url']))
    count_tld_url = str(count_tld(dict_url['url']))
    # DOMAIN
    dot_host = str(count(dict_url['host'], '.'))
    hyphe_host = str(count(dict_url['host'], '-'))
    underline_host = str(count(dict_url['host'], '_'))
    bar_host = str(count(dict_url['host'], '/'))
    question_host = str(count(dict_url['host'], '?'))
    equal_host = str(count(dict_url['host'], '='))
    arroba_host = str(count(dict_url['host'], '@'))
    ampersand_host = str(count(dict_url['host'], '&'))
    exclamation_host = str(count(dict_url['host'], '!'))
    blank_host = str(count(dict_url['host'], ' '))
    til_host = str(count(dict_url['host'], '~'))
    comma_host = str(count(dict_url['host'], ','))
    plus_host = str(count(dict_url['host'], '+'))
    asterisk_host = str(count(dict_url['host'], '*'))
    hashtag_host = str(count(dict_url['host'], '#'))
    money_sign_host = str(count(dict_url['host'], '$'))
    percentage_host = str(count(dict_url['host'], '%'))
    vowels_host = str(count_vowels(dict_url['host']))
    len_host = str(length(dict_url['host']))
    ip_exist = str(valid_ip(dict_url['host']))
    server_client = str(check_word_server_client(dict_url['host']))
    # DIRECTORY
    if dict_url['path']:
        dot_path = str(count(dict_url['path'], '.'))
        hyphe_path = str(count(dict_url['path'], '-'))
        underline_path = str(count(dict_url['path'], '_'))
        bar_path = str(count(dict_url['path'], '/'))
        question_path = str(count(dict_url['path'], '?'))
        equal_path = str(count(dict_url['path'], '='))
        arroba_path = str(count(dict_url['path'], '@'))
        ampersand_path = str(count(dict_url['path'], '&'))
        exclamation_path = str(count(dict_url['path'], '!'))
        blank_path = str(count(dict_url['path'], ' '))
        til_path = str(count(dict_url['path'], '~'))
        comma_path = str(count(dict_url['path'], ','))
        plus_path = str(count(dict_url['path'], '+'))
        asterisk_path = str(count(dict_url['path'], '*'))
        hashtag_path = str(count(dict_url['path'], '#'))
        money_sign_path = str(count(dict_url['path'], '$'))
        percentage_path = str(count(dict_url['path'], '%'))
        len_path = str(length(dict_url['path']))
    else:
        dot_path = 0
        hyphe_path = 0
        underline_path = 0
        bar_path = 0
        question_path = 0
        equal_path = 0
        arroba_path = 0
        ampersand_path = 0
        exclamation_path = 0
        blank_path = 0
        til_path = 0
        comma_path = 0
        plus_path = 0
        asterisk_path = 0
        hashtag_path = 0
        money_sign_path = 0
        percentage_path = 0
        len_path = 0
    # FILE
    if dict_url['path']:
        dot_file = str(count(posixpath.basename(dict_url['path']), '.'))
        hyphe_file = str(count(posixpath.basename(dict_url['path']), '-'))
        underline_file = str(count(posixpath.basename(dict_url['path']), '_'))
        bar_file = str(count(posixpath.basename(dict_url['path']), '/'))
        question_file = str(count(posixpath.basename(dict_url['path']), '?'))
        equal_file = str(count(posixpath.basename(dict_url['path']), '='))
        arroba_file = str(count(posixpath.basename(dict_url['path']), '@'))
        ampersand_file = str(count(posixpath.basename(dict_url['path']), '&'))
        exclamation_file = str(count(posixpath.basename(dict_url['path']), '!'))
        blank_file = str(count(posixpath.basename(dict_url['path']), ' '))
        til_file = str(count(posixpath.basename(dict_url['path']), '~'))
        comma_file = str(count(posixpath.basename(dict_url['path']), ','))
        plus_file = str(count(posixpath.basename(dict_url['path']), '+'))
        asterisk_file = str(count(posixpath.basename(dict_url['path']), '*'))
        hashtag_file = str(count(posixpath.basename(dict_url['path']), '#'))
        money_sign_file = str(count(posixpath.basename(dict_url['path']), '$'))
        percentage_file = str(count(posixpath.basename(dict_url['path']), '%'))
        len_file = str(length(posixpath.basename(dict_url['path'])))
        extension = LANG_MAP[str(extract_extension(posixpath.basename(dict_url['path'])))]
    else:
        dot_file = 0
        hyphe_file = 0
        underline_file = 0
        bar_file = 0
        question_file = 0
        equal_file = 0
        arroba_file = 0
        ampersand_file = 0
        exclamation_file = 0
        blank_file = 0
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
        dot_params = str(count(dict_url['query'], '.'))
        hyphe_params = str(count(dict_url['query'], '-'))
        underline_params = str(count(dict_url['query'], '_'))
        bar_params = str(count(dict_url['query'], '/'))
        question_params = str(count(dict_url['query'], '?'))
        equal_params = str(count(dict_url['query'], '='))
        arroba_params = str(count(dict_url['query'], '@'))
        ampersand_params = str(count(dict_url['query'], '&'))
        exclamation_params = str(count(dict_url['query'], '!'))
        blank_params = str(count(dict_url['query'], ' '))
        til_params = str(count(dict_url['query'], '~'))
        comma_params = str(count(dict_url['query'], ','))
        plus_params = str(count(dict_url['query'], '+'))
        asterisk_params = str(count(dict_url['query'], '*'))
        hashtag_params = str(count(dict_url['query'], '#'))
        money_sign_params = str(count(dict_url['query'], '$'))
        percentage_params = str(count(dict_url['query'], '%'))
        len_params = str(length(dict_url['query']))
        tld_params = str(check_tld(dict_url['query']))
        number_params = str(count_params(dict_url['query']))
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
        blank_params = 0
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
    blacklist_url = 0#str(check_blacklists(dict_url['protocol'] + '://' + dict_url['url']))
    blacklist_ip = 0#str(check_blacklists_ip(dict_url))
    blacklist_domain = 0#str(check_blacklists(dict_url['protocol'] + '://' + dict_url['host']))

    """HOST"""
    spf = str(valid_spf(dict_url['host']))
    rbl = str(check_rbl(dict_url['host']))
    time_domain = str(check_time_response(dict_url['protocol'] + '://' + dict_url['host']))
    asn = str(get_asn_number(dict_url))
    country = COUNTRY_MAP[str(get_country(dict_url))]
    ptr = str(get_ptr(dict_url))
    activation_time = str(time_activation_domain(dict_url))
    expiration_time = str(expiration_date_register(dict_url))
    count_ip = str(count_ips(dict_url))
    count_ns = str(count_name_servers(dict_url))
    count_mx = str(count_mx_servers(dict_url))
    ttl = str(extract_ttl(dict_url))

    """OTHERS"""
    ssl = str(check_ssl('https://' + dict_url['url']))
    count_redirect = str(count_redirects(
        dict_url['protocol'] + '://' + dict_url['url']))
    google_url = 0#str(google_search(dict_url['url']))
    google_domain = 0#str(google_search(dict_url['host']))
    shortener = str(check_shortener(dict_url))

    _lexical = [
        dot_url, hyphe_url, underline_url, bar_url, question_url,
        equal_url, arroba_url, ampersand_url, exclamation_url,
        blank_url, til_url, comma_url, plus_url, asterisk_url, hashtag_url,
        money_sign_url, percentage_url, count_tld_url, len_url, dot_host,
        hyphe_host, underline_host, bar_host, question_host, equal_host,
        arroba_host, ampersand_host, exclamation_host, blank_host, til_host,
        comma_host, plus_host, asterisk_host, hashtag_host, money_sign_host,
        percentage_host, vowels_host, len_host, ip_exist, server_client,
        dot_path, hyphe_path, underline_path, bar_path, question_path,
        equal_path, arroba_path, ampersand_path, exclamation_path,
        blank_path, til_path, comma_path, plus_path, asterisk_path,
        hashtag_path, money_sign_path, percentage_path, len_path, dot_file,
        hyphe_file, underline_file, bar_file, question_file, equal_file,
        arroba_file, ampersand_file, exclamation_file, blank_file,
        til_file, comma_file, plus_file, asterisk_file, hashtag_file,
        money_sign_file, percentage_file, len_file, dot_params,
        hyphe_params, underline_params, bar_params, question_params,
        equal_params, arroba_params, ampersand_params, exclamation_params,
        blank_params, til_params, comma_params, plus_params, asterisk_params,
        hashtag_params, money_sign_params, percentage_params, len_params,
        tld_params, number_params, email_exist, extension
    ]

    _blacklist = [blacklist_url, blacklist_ip, blacklist_domain]

    _host = [rbl, time_domain, spf, country, asn, ptr, activation_time,
                expiration_time, count_ip, count_ns, count_mx, ttl]

    _others = [ssl, count_redirect, google_url, google_domain, shortener]

    result = []
    result.extend(_lexical)
    result.extend(_blacklist)
    result.extend(_host)
    result.extend(_others)
    result.extend([''])
    result = [result[index] for index in PRODUCTION_COLUMNS]
    for n, i in enumerate(result):
        if i == 'True':
            result[n]=1
        elif i == 'False':
            result[n]=0
        elif i == '?':
            result[n]=0
        else:
            result[n] = float(result[n])
    return result


def main(urls, dataset, phishing):
    with open(dataset, "w") as output:
        writer = csv.writer(output)
        writer.writerow(attributes())
        for url in read_file(urls):
            print(f"extracting feature from {url}...")
            result = extract_features(url)
            result.append(phishing)
            writer.writerow(result)
            print(f"extracted features from {url}...")


if __name__ == "__main__":
    extract_features("https://bcwfek.nut.cc/,,,,,,,,,")
