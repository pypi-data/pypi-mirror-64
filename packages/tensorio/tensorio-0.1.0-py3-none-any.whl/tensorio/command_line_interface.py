#!/usr/bin/env python

import argparse

from termcolor import cprint

import tensorio.cli.bundle.arg_parser
import tensorio.cli.convert.arg_parser

import tensorio.cli.bundle.executor
import tensorio.cli.convert.executor

from tensorio.cli.utils.exceptions import ExecutorException

def generate_arg_parser():
  """
  Prepares the tensor/io cli arguments parser.
  """

  parser = argparse.ArgumentParser(description='The tensor/io python package command line interface')
  
  subparsers = parser.add_subparsers(dest='command')
  subparsers.required = True

  tensorio.cli.bundle.arg_parser.add_subparsers(subparsers)
  tensorio.cli.convert.arg_parser.add_subparsers(subparsers)

  return parser

def main():
  """
  Main entry point to the tensor/io cli. See setup.py:entry_points.
  """

  parser = generate_arg_parser()
  args = parser.parse_args()

  try:
    if args.command == 'bundle':
      tensorio.cli.bundle.executor.run(args)
    elif args.command == 'convert':
      tensorio.cli.convert.executor.run(args)
    else:
      raise GeneratorException('Unknown command')
  except ExecutorException as error:
    cprint(error, 'red')
