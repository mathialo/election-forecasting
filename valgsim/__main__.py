import argparse

from valgsim.model import run_model


def main() -> None:
    argparser = argparse.ArgumentParser("model")
    argparser.add_argument("epochs", type=int, help="Number of iterations")
    argparser.add_argument("simulations", type=int, help="Number of simulated elections pr iteration")
    argparser.add_argument("--no-load", action="store_true", help="Don't start by loading remote data")
    argparser.add_argument(
        "--poll-from", type=str, help="Timestamp (yyyy-mm-dd) of when to gather polling data from", default="2021-06-01"
    )
    argparser.add_argument(
        "--election-date", type=str, help="Timestamp (yyyy-mm-dd) of when to simulate election", default="2021-09-13"
    )

    args = argparser.parse_args()

    run_model(
        epochs=args.epochs,
        simulations=args.simulations,
        skip_load=args.no_load,
        poll_from=args.poll_from,
        poll_to=args.election_date,
        election_date=args.election_date,
    )


if __name__ == "__main__":
    main()
