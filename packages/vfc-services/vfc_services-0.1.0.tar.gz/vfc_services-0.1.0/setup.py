from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='vfc_services',
      version='0.1.0',
      description='Easily have access to all VFC microservices',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/kpnic-vfc/vfc-services',
      author='Robert Boes',
      author_email='robert.boes@kpn.com',
      license='MIT',
      packages=['vfc_services'],
      zip_safe=False,
      python_requires='>=3.7',
)
