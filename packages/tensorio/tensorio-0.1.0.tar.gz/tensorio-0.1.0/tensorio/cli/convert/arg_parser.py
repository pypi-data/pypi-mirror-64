import argparse

def add_subparsers(subparsers):
  """
  Prepares the convert subcommand arguments parser.
  """

  convert_subparser = subparsers.add_parser('convert')

  convert_subparser.add_argument(
    '--from',
    '-f',
    choices=['tensorflow'],
    dest='from_format',
    required=True,
    help='The format to convert from',
    )

  convert_subparser.add_argument(
    '--to',
    '-t',
    choices=['tflite'],
    dest='to_format',
    required=True,
    help='The format to convert to'
    )

  convert_subparser.add_argument(
    '--input',
    '-i',
    required=True,
    help='Path to the model which will be converted (GCS paths allowed)'
  )

  convert_subparser.add_argument(
    '--output',
    '-o',
    required=True,
    help='Path to the output destination, which will be created (GCS paths allowed)'
  )

  