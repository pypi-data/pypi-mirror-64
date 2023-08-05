#!/usr/bin/env python

from distutils.core import setup

with open("README.rst") as long_description_file:
    setup(name="MDocument",
          version="0.2",
          description="Simple DRM for motor client",
          author="Yurzs",
          author_email="yurzs+MDocument@icloud.com",
          packages=["MDocument"],
          install_requires=["motor"],
          license="MIT",
          long_description=long_description_file.read(),
          keywords=["mongo", "motor", "DRM"],
          url="https://git.yurzs.dev/MDocument",
          classifiers=[
              "Development Status :: 3 - Alpha",
              "License :: OSI Approved :: MIT License",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
          ])
