from setuptools import setup, find_packages

setup(name='flask_restplus_data',
      version='0.0.2',
      description='Library inspired by Spring Data to perform Operations on datastores',
      license='MIT',
      url='https://github.com/nucklehead/flask-restplus-data',
      download_url='https://github.com/nucklehead/flask-restplus-data/tarball/0.0.1',
      author='nucklehead',
      author_email='pierevans@gmail.com',
      keywords=[
          'datastore', 'sql', 'nosql', 'postgres', 'mysql', 'sqlite', 'obdc', 'oracle database', 'mongodb', 'orm',
          'flask'
          , 'flask_restplus', 'rest', 'restplus'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Framework :: Flask',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      packages=find_packages(exclude=['test']),
      install_requires=[
          'confuse==1.0.0',
          'psycopg2-binary==2.7.7',
          'flask-sqlalchemy==2.4.1',
          'Flask-MongoAlchemy==0.7.2',
          'yoyo-migrations==6.1.0',
      ])
