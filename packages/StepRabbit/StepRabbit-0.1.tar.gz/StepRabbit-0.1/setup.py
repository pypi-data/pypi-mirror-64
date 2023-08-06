from setuptools import setup

setup(name='StepRabbit',
      version='0.1',
          long_description='long_description',
	long_description_content_type="text/markdown",
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
