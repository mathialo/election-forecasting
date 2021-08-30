import argparse

from valgsim.model import run_model


def main() -> None:
    argparser = argparse.ArgumentParser("model")
    argparser.add_argument("runs", type=int)

    args = argparser.parse_args()

    run_model(args.runs)


if __name__ == "__main__":
    main()
