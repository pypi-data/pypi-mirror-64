import setuptools

setuptools.setup(
  name='tensorio',
  version='0.1.1',
  author='doc.ai',
  author_email='philip@doc.ai',
  description='Tensor/IO python utilities',
  license='Apache License 2.0',
  url='https://github.com/doc-ai/tensorio-python-package',
  packages=[
    'tensorio',
    'tensorio.cli',
    'tensorio.cli.bundle',
    'tensorio.cli.convert',
    'tensorio.cli.utils',
    'tensorio.model_bundle',
    'tensorio.convert'
  ],
  install_requires=[
    'tensorflow',
    'termcolor'
  ],
  entry_points={
    'console_scripts': ['tio=tensorio.command_line_interface:main']
  },
  classifiers=[
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
  ],
)