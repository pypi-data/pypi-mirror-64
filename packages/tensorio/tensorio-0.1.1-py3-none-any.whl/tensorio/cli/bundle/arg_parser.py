import argparse

def add_subparsers(subparsers):
  """
  Prepares the bundle subcommand arguments parser.
  """

  bundle_group = subparsers.add_parser('bundle')
  bundle_subparser = bundle_group.add_subparsers(dest='subcommand')
  bundle_subparser.required = True

  # create

  create_subparser = bundle_subparser.add_parser('create')

  # name of the output bundle is required

  create_subparser.add_argument( 
    '--name',
    '-n',
    required=True,
    help='Name of the bundle, used for the name of the bundle root directory'
  )

  # model is either a savedmodel directory or a tflite binary

  create_subparser.add_argument(
    '--model',
    '-m',
    required=True,
    help='Path to directory containing SavedModel pb file and variables, or path to TFLite binary (GCS paths allowed)'
  )

  # model.json contains the tensor/io metadata about the underlying model

  create_subparser.add_argument(
    '--json',
    '-j',
    required=True,
    help='Path to a Tensor/IO model.json file'
  )

  # assets directory is optional

  create_subparser.add_argument(
    '--assets',
    '-a',
    required=False,
    help='Path to a Tensor/IO assets directory'
  )

  # name of the output zip file is optional defaults to {name}.zip

  create_subparser.add_argument(
    '--outfile',
    '-o',
    required=False,
    help='Path at which tiobundle zipfile should be created; defaults to {bundle-name}.zip (GCS paths allowed)'
  )

  # info

  info_subparser = bundle_subparser.add_parser('info')
