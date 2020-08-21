import numpy as np

from extract import extract_features
from tensorflow import keras


FEATURES_NAMES = ['dot_url', 'hyphe_url', 'underline_url', 'bar_url', 'question_url', 'equal_url', 'arroba_url', 'ampersand_url', 'exclamation_url', 'til_url', 'comma_url', 'plus_url', 'asterisk_url', 'hashtag_url', 'money_sign_url', 'percentage_url', 'count_tld_url', 'len_url', 'dot_host', 'hyphe_host', 'underline_host', 'arroba_host', 'vowels_host', 'len_host', 'ip_exist', 'server_client', 'dot_path', 'hyphe_path', 'underline_path', 'bar_path', 'equal_path', 'arroba_path', 'ampersand_path', 'exclamation_path', 'til_path', 'comma_path', 'plus_path', 'asterisk_path', 'money_sign_path', 'percentage_path', 'len_path', 'dot_file', 'hyphe_file', 'underline_file', 'equal_file', 'arroba_file', 'ampersand_file', 'exclamation_file', 'til_file', 'comma_file', 'plus_file', 'asterisk_file', 'hashtag_file', 'money_sign_file', 'percentage_file', 'len_file', 'dot_params', 'hyphe_params', 'underline_params', 'bar_params', 'question_params', 'equal_params', 'arroba_params', 'ampersand_params', 'exclamation_params', 'til_params', 'comma_params', 'plus_params', 'asterisk_params', 'hashtag_params', 'money_sign_params', 'percentage_params', 'len_params', 'tld_params', 'number_params', 'email_exist', 'extension', 'rbl', 'time_domain', 'spf', 'country', 'activation_time', 'expiration_time', 'count_ip', 'count_ns', 'count_mx', 'ttl', 'ssl', 'count_redirect', 'google_url', 'google_domain']
model = keras.models.load_model("url_phishing.h5")


def predict_single(data):
    return list(list(np.round(model.predict(np.array([np.array([data]).reshape((91,1))])))[0]))


def predict(url):
    features = extract_features(url)
    features_dict = {}
    for i in range(len(FEATURES_NAMES)):
        features_dict[FEATURES_NAMES[i]] = features[i]
    print(predict_single(features))


if __name__ == "__main__":
    urls = [
        "flixster.com/photos/olga-mironova-olga-mironova-12985823",
        "http://recoverycheck96.000webhostapp.com/Payment-update-0.html?=100658",
        "http://recoverycheck96.000webhostapp.com/Payment-update-0.html?=100658,,,,,,,,,",
    ]
    for url in urls:
        predict(url)
