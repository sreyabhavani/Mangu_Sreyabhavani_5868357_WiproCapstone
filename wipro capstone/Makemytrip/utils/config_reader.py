import configparser


class ConfigReader:

    config = configparser.RawConfigParser()

    config.read("config/config.properties")

    @classmethod
    def get(cls, key):

        return cls.config.get(
            "DEFAULT",
            key
        )