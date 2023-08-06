from setuptools import setup

setup(name='KLWrappers',
      version='1.0.0',
      py_modules=["UploadWrappers"],
      package_dir={'': 'src'},
      install_requires=["paho-mqtt", "kafka-python"])
