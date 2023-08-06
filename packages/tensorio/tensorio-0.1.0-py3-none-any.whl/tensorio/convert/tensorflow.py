import tensorflow as tf

FORMAT_TENSORFLOW = 'tensorflow'
FORMAT_TFLITE     = 'tflite'

class TensorflowConverterFormatException(Exception):
  """
  Raised if the conversion to format is not valid
  """
  pass

class TensorflowConverterOutputFileExistsException(Exception):
  """
  Raised if the target output file already exists
  """
  pass

class TensorflowConverterSavedModelMisspecificationError(Exception):
  """
  Raised if the specified saved model directory does not exist or is 
  not a directory
  """
  pass

def convert(to_format, model_dir, output_file):
  """
  Primary entry point for the tensorflow converter

  Args:
  1. to_format - The target format for conversion
  2. model_dir - The saved model driectory containing a savedmodel.pb and a variables folder
  3. output_file - The name of the output file

  Returns: None
  """
  
  # input ouput file error checking

  if tf.io.gfile.exists(output_file):
    raise TFLiteFileExistsError('ERROR: Specified TFLite binary path ({}) already exists'.format(output_file))
  if not tf.io.gfile.exists(model_dir) or not tf.io.gfile.isdir(model_dir):
    raise TensorflowConverterSavedModelMisspecificationError('ERROR: Specified SavedModel directory ({}) either does not exist or is not a directory'.format(model_dir)) 
  
  # branch on target format

  if to_format == FORMAT_TFLITE:
    convert_to_tflite(model_dir, output_file)
  else:
    raise TensorflowConverterFormatException('ERROR: Specified target format ({}) is not valid'.format(to_format)) 

def convert_to_tflite(model_dir, output_file):
  """
  Converts a tensorflow saved model to a tflite binary

  Args:
  1. model_dir - The saved model driectory containing a savedmodel.pb and a variables folder
  2. output_file - The name of the output file

  Returns: None
  """

  converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
  tflite_model = converter.convert()
  
  with tf.io.gfile.GFile(output_file, 'wb') as f:
    f.write(tflite_model)

