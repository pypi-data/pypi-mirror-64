import fire

import tully.networking as networking


class Cli:
    def __init__(self):
        self.networking = networking


def main():
    fire.Fire(Cli())
