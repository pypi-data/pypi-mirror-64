import argparse
import asyncio

from . import start_udp_client


def main_udp(args: argparse.Namespace) -> None:
    coro = start_udp_client(args.host, args.port, count=args.count, payload_size=args.packetsize, wait=args.wait)
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        loop.run_until_complete(task)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_udp_ping = subparsers.add_parser('udp')
    parser_udp_ping.add_argument('host')
    parser_udp_ping.add_argument('port', type=int)
    parser_udp_ping.add_argument('-c', '--count', type=int, default=-1)
    parser_udp_ping.add_argument('-s', '--packetsize', type=int, default=0)
    parser_udp_ping.add_argument('-i', '--wait', type=float, default=1.0)
    parser_udp_ping.set_defaults(func=main_udp)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
