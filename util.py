import os


class Util:
    def __init(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_root_dir(self):
        return self.ROOT_DIR

    @staticmethod
    def day_to_milliseconds(days):
        return days * 24 * 60 * 60 * 1000
