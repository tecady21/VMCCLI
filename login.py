import configparser
import getpass
import datetime
import requests

LOGIN_URL = "https://vmchecker.cs.pub.ro/services/services.py/login"
CONFIG_FILE = "config.ini"
BASE_CONFIGS = {
    "cookie": str(None),
    "last-saved": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "username": str(None),
}
TIMEOUT = 5


def get_config_file():
    config_parser = configparser.ConfigParser()

    try:
        open(CONFIG_FILE, "r")
        config_parser.read(CONFIG_FILE)
    except FileNotFoundError:
        with open(CONFIG_FILE, "w") as f:
            config_parser["LOGIN"] = BASE_CONFIGS
            config_parser.write(f)
            config_parser.read(CONFIG_FILE)

    return config_parser


def get_cookie(username):
    password = getpass.getpass("Password:")
    data = {'username': username, 'password': password}

    response = requests.post(LOGIN_URL, data=data)
    if response.status_code != 200:
        print("Request error with status code " + str(response.status_code))
        exit(1)

    json_response = response.json()

    if json_response['status'] is False:
        print("Failed to login")
        return None
    else:
        cookie_raw = response.headers['Set-Cookie']
        if cookie_raw is not None:
            return cookie_raw.split(";")[0]


def login_session():
    config = get_config_file()

    username = config["LOGIN"]["username"]
    if username == str(None):
        print("Set up your username using vmccli setname username.")
        return False

    last_time_diff = datetime.datetime.now() - datetime.datetime.strptime(config["LOGIN"]["last-saved"], "%Y-%m-%d %H:%M:%S")

    # Check if we have a saved cookie
    # If there is no cookie or cookie is expired, get a new one, else read from config file
    if config["LOGIN"]["cookie"] == str(None) or last_time_diff.total_seconds() / 60 > TIMEOUT:
        print("Cookie expired or none. Need to login to get a cookie.")
        # Get a new cookie then update the timestamp
        cookie = config["LOGIN"]["cookie"] = get_cookie(username)
        config["LOGIN"]["last-saved"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        cookie = config["LOGIN"]["cookie"]

    # Updating config file
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    return cookie


def set_name(username):
    config = get_config_file()

    config["LOGIN"]["username"] = username

    with open(CONFIG_FILE, "w") as f:
        config.write(f)


