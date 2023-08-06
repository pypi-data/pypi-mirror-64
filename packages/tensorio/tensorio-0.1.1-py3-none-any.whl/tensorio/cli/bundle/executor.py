import os

from tensorio.model_bundle import bundler
from tensorio.cli.utils.exceptions import ExecutorException

def run(args):
  """
  Primary entry point to the tensor/io bundle subcommand.
  """
  
  if args.subcommand == 'create':
    run_create(args)
  elif args.subcommand == 'info':
    run_info(args)
  else:
    raise ExecutorException('Error: {subcommand} is not a valid command.'.format(subcommand=args.subcommand))

def run_create(args):
  
  # Ensure bundle name has .tiobundle extension

  bundle_name = args.name
  bundle_ext = os.path.splitext(args.name)[1]

  if bundle_ext != '.tiobundle':
    bundle_name = '{}.tiobundle'.format(bundle_name)

  # Determine name of final zipfile
  
  if args.outfile is None:
    zipfile = '{}.zip'.format(bundle_name)
  else:
    zipfile = args.outfile

  # Bundle

  print('bundle: {}, model: {}, model.json: {}, assets directory: {}, zipfile: {}'.format(
    bundle_name,
    args.model,
    args.json,
    args.assets,
    zipfile
  ))

  zipfile = bundler.create_bundle(bundle_name, args.model, args.json, args.assets, zipfile)
  print('Wrote zipped bundle to {}'.format(zipfile))

def run_info(args):
  pass