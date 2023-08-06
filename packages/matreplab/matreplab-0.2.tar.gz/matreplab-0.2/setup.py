import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='matreplab',  
  version='0.2',
  scripts=['matREPLab'] ,
  author="Robin Tournemenne",
  author_email="rtournem@lavabit.com",
  description="A better matlab -nodesktop",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/RobinTournemenne/matREPLab",
  packages=setuptools.find_packages(),
  install_requires=[
      'pexpect',
      'pygments',
      'prompt_toolkit',
      'pathlib'
  ],
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
 )