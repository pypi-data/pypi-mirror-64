# Tensor/IO Python Utilities

## Command Line Interface

### Bundle

The bundle command packages model files, model metadata, and assets into a *tiobundle* for use with Tensor/IO.

A *tiobundle* is just a folder with all the information needed to run a model on device with Tensor/IO. It includes the underlying model in one of the supported formats, a *model.json* file containing descriptions of the model's inputs and outputs, and any associated model assets.

For more information on the format see Tensor/IO's [Packaging Model's Wiki](https://github.com/doc-ai/tensorio-ios/wiki/Packaging-Models).

**Usage**

```
tio bundle create --name {bundle_name.tiobundle} --model {modle_dir_or_binary} --json {model.json} --assets {optional_assets}
```

### Convert

The convert command aids in the process of converting models from one format to another prior to being packaged into a *tiobundle*. Currently you may only convert from TensorFlow SavedModel exports to TF Lite binaries.

In cases where a more complex conversion is required it may be necessary to follow the instructions at Tensor/IO's [TensorFlow Lite Backend Wiki](https://github.com/doc-ai/tensorio-ios/wiki/TensorFlow-Lite-Backend).

**Usage**

```
tio convert --from tensorflow --to tflite --input {saved_model_dir} --output {filename.tflite}
```

## Modules

The functions called by the command line interface are also available directly to python code via the package's submodules.

### model_bundle

The submodule responsible for packaging data into a *tiobundle*. You may pass GCS paths for any filepath.

**Usage**

```python
from tensorio.model_bundle import bundler

name = 'name_of_bundle.tiobundle'
model = 'path/to/model_dir_or_file'
model_json = 'path/to/model.json'
assets = 'path/to/optional/assets'
zipfile = 'path/to/target_zipfile'

zipfile_path = bundler.create_bundle(name, model, model_json, assets, zipfile)
```

Note that assets may be `None` and that the returned `zipfile_path` should be the same as the `zipfile` path passed into the function.

### convert

The submodule responsible for converting from one model format to another. You may pass GCS paths for the input and output files.

**Usage**

```python
import tensorio.convert.tensorflow

to_format = 'tflite'
input_file = 'path/to/saved_model_dir/'
output_file = 'path/to/target_model.tflite'

tensorio.convert.tensorflow.convert(to_format, input_file, output_file)

```