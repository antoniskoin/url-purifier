import configparser


def load_config() -> dict:
    config = configparser.ConfigParser()
    config.read("configuration.cfg")

    username = config.get("DATABASE", "USERNAME")
    password = config.get("DATABASE", "PASSWORD")

    config = {"username": username, "password": password}
    return config
