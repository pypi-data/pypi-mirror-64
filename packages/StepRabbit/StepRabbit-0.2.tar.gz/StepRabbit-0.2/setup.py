from setuptools import setup

setup(name='StepRabbit',
      version='0.2',
      description='Code snippets communicator',
      install_requires=[
          'pika',
          'uuid',
    ],
	download_url = "https://github.com/Kaporos/StepRabbit",
	  keywords = ['step', 'snippets', 'rabbitmq'],   # Keywords that define your package best
	package="name",
      author='Théo Daroun',
      author_email='mail@tdaron.tk',
      license='MIT',
      packages=['StepRabbit'],
      zip_safe=False)
