import argparse


def cli():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    cli()
