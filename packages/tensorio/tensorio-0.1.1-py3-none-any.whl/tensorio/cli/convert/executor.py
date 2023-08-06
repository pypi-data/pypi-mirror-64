import tensorio.convert.tensorflow
from tensorio.cli.utils.exceptions import ExecutorException

FORMAT_TENSORFLOW = 'tensorflow'
FORMAT_TFLITE     = 'tflite'

def run(args):
  """
  Primary entry point to the tensor/io bundle subcommand.
  """
  
  print('input format: {}, output format: {}, in file: {}, out file: {}'.format(
    args.from_format,
    args.to_format,
    args.input,
    args.output
  ))

  if args.from_format == FORMAT_TENSORFLOW:
    tensorio.convert.tensorflow.convert(
      args.to_format,
      args.input,
      args.output
      )
  else:
    raise ExecutorException('Error: from or to format is not valid.')
  