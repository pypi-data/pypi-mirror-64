#!/usr/bin/env python
import datetime
from distutils.core import setup

with open("README.rst") as long_description_file:
    setup(name="MDocument",
          version="0.5.{0}".format(datetime.datetime.now().timestamp()),
          description="Simple DRM for motor client",
          author="Yurzs",
          author_email="yurzs+MDocument@yurzs.dev",
          packages=["MDocument"],
          install_requires=["motor"],
          license="MIT",
          long_description=long_description_file.read(),
          keywords=["mongo", "motor", "DRM"],
          url="https://git.yurzs.dev/yurzs/MDocument",
          classifiers=[
              "Development Status :: 3 - Alpha",
              "License :: OSI Approved :: MIT License",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
          ])
