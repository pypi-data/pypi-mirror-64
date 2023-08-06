from setuptools import setup

setup(name='KLWrappers',
      version='0.0.1',
      py_modules=["UploadWrappers"],
      package_dir={'': 'src'},
      install_requires=["paho-mqtt", "json", "kafka-python"])
