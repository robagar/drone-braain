from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='drone_braain',
      version='0.0.1',
      description='Tello drone AI',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/robagar/drone_braain',
      project_urls={
      },
      author='Rob Agar',
      author_email='tello_asyncio@fastmail.net',
      license='GPL',
      packages=['drone_braain'],
      zip_safe=False,
      python_requires=">=3.6")