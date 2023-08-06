import argparse
import logging.config

from edeklaracje_client.client import EDeklaracjeClient, Environment


def setup_verbose_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'zeep.transports': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': ['console'],
            },
        }
    })


def send_declaration(args):
    client = EDeklaracjeClient(Environment.PRODUCTION)
    with open(args.file) as f:
        ref_id = client.send_document(f.read())
        print("Declaration sent. RefId: {}".format(ref_id))
        print("Waiting for UPO...")
        upo = client.wait_for_upo(ref_id, timeout_in_seconds=args.timeout_in_seconds)
        print(upo)


def wait_for_upo(args):
    client = EDeklaracjeClient(Environment.PRODUCTION)
    print("Waiting for UPO...")
    upo = client.wait_for_upo(args.refId, timeout_in_seconds=args.timeout_in_seconds)
    print(upo)


def _add_common_args(parser):
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-t", "--timeout_in_seconds", help="time (in seconds) to wait for document processing on eDeklaracje side", type=int, default=600)


def main():
    parser = argparse.ArgumentParser(description='Send declaration to eDeklaracje')
    subparsers = parser.add_subparsers(required=True, dest='command')
    document_send_parser = subparsers.add_parser('send_document', help="Sends document and waits for UPO")
    document_send_parser.add_argument('file', type=str, help='path to the xml file with declaration')
    document_send_parser.set_defaults(command=send_declaration)
    _add_common_args(document_send_parser)
    wait_for_upo_parser = subparsers.add_parser('wait_for_upo', help="Waits for UPO for a given refId")
    wait_for_upo_parser.add_argument('refId', type=str, help='refId to wait on')
    wait_for_upo_parser.set_defaults(command=wait_for_upo)
    _add_common_args(wait_for_upo_parser)
    args = parser.parse_args()
    if args.verbose:
        setup_verbose_logging()
    args.command(args)


if __name__ == "__main__":
    main()
