import tempfile
import shutil
import json
import os

import tensorflow as tf

ASSETS_DIR          = 'assets'
MODEL_JSON_FILENAME = 'model.json'

class ZippedTIOBundleExistsError(Exception):
  """
  Raised in the process of a zipped tiobundle build if a file (or directory) already exists
  at the specified build path.
  """
  pass

class ZippedTIOBundleMisspecificationError(Exception):
  """
  Raised in the process of a zipped tiobundle build if one or more of:
  1. model.json
  2. model filepath
  does not exist as a file.
  """
  pass

class InvalidModelJSONSpecification(Exception):
  """
  Raised if the bundle specification (e.g. model.json) is invalid.
  """
  pass

def create_bundle(bundle_name, model_path, json_path, assets_path, zipfile):
  """
  Builds zipped tiobundle file for Tensor/IO deployments

  Args:
  1. bundle_name - Name of the bundle
  2. model_path - Path to TF Lite binary or TensorFlow SavedModel directory
  3. json_path - Path to Tensor/IO bundle model.json file
  4. assets_path - Path to Tensor/IO bundle assets directory, may be None
  5. zipfile - Path of the final zip file that contains the bundle

  Returns: zipfile path if the zipped tiobundle was created successfully
  """

  # Ensure bundle_name has .tiobundle extension

  bundle_ext = os.path.splitext(bundle_name)[1]

  if bundle_ext != '.tiobundle':
    bundle_name = '{}.tiobundle'.format(bundle_name)

  # Filepath error checking

  if tf.io.gfile.exists(zipfile):
    raise ZippedTIOBundleExistsError('ERROR: Specified zipped tiobundle output path ({}) already exists'.format(zipfile))

  if not tf.io.gfile.exists(model_path):
    raise ZippedTIOBundleMisspecificationError('ERROR: Model path ({}) does not exist'.format(model_path))

  if not tf.io.gfile.exists(json_path) or tf.io.gfile.isdir(json_path):
    raise ZippedTIOBundleMisspecificationError('ERROR: model.json path ({}) either does not exist or is not a file'.format(model_path))

  # Read model.json

  with tf.io.gfile.GFile(json_path, 'rb') as f:
    bundle_spec = json.loads(f.read().decode('utf-8'))

  # Extract model.name from spec

  model_spec = bundle_spec.get('model')

  if model_spec is None:
    raise InvalidModelJSONSpecification('No "model" key at root level of model.json')

  model_name = model_spec.get('file')

  if model_name is None:
    raise InvalidModelJSONSpecification('No "file" specified under "model" key of model.json')

  # Prepare temporary bundle directory

  scratch_dir = tempfile.mkdtemp()
  bundle_dir = os.path.join(scratch_dir, bundle_name)
  os.mkdir(bundle_dir)

  # Copy model

  bundle_model_path = os.path.join(bundle_dir, model_name)

  if tf.io.gfile.isdir(model_path):
    tf.io.gfile.mkdir(bundle_model_path)
    _copy_dir_contents(model_path, bundle_model_path)
  else:
    tf.io.gfile.copy(model_path, bundle_model_path)

  # Copy model.json

  bundle_model_json_path = os.path.join(bundle_dir, MODEL_JSON_FILENAME)
  tf.io.gfile.copy(json_path, bundle_model_json_path)

  # Copy assets

  if assets_path != None:
    bundle_assets_path = os.path.join(bundle_dir, ASSETS_DIR)
    tf.io.gfile.mkdir(bundle_assets_path)
    _copy_dir_contents(assets_path, bundle_assets_path)

  # Zip

  scratch_zipfile = os.path.join(scratch_dir, os.path.splitext(os.path.basename(os.path.normpath(zipfile)))[0])
  scratch_zipfile = '{}.zip'.format(scratch_zipfile)
  
  _make_archive(bundle_dir, scratch_zipfile)

  # Copy zipped file and cleanup
  
  tf.io.gfile.copy(scratch_zipfile, zipfile)
  shutil.rmtree(scratch_dir)

  return zipfile

def _copy_dir_contents(src, dst):
  """
  Copies the contents of directory src to directory dst. Source and destination must already exist.
  They may be located on GCS.

  Args:
  1. src - The source directory whose contents will be copied
  2. dst - The destination directory whose contents will be copied

  Returns: None
  """
  
  contents = tf.io.gfile.glob(os.path.join(src, '*'))

  for filename in contents:
    basename = os.path.basename(filename)

    src_file = filename
    dst_file = os.path.join(dst, basename)

    if tf.io.gfile.isdir(filename):
      tf.io.gfile.mkdir(dst_file)
      _copy_dir_contents(src_file, dst_file)
    else:
      tf.io.gfile.copy(src_file, dst_file)

def _make_archive(source, destination):
  """
  Wrappewr around shutil.make_archive, which is confusing and easy to use incorrectly.

  Args:
  1. source - The folder you want to zip up
  2. destination - The path to the zipfile that will be created, including the extension

  Returns: None
  """

  base = os.path.basename(destination)  
  name, format = os.path.splitext(base)
  format = format[1:]

  archive_from = os.path.dirname(source)
  archive_to = os.path.basename(source.strip(os.sep))
  
  shutil.make_archive(name, format, archive_from, archive_to)
  shutil.move('%s.%s'%(name,format), destination)