from setuptools import setup

setup(name='test1288',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='zeeshan',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['test1288'],
      install_requires=[
          'requests',
          'firebase_admin',
      ],
      zip_safe=False,
      include_package_data=True)