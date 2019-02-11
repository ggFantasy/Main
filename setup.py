from setuptools import setup

setup(
    name='ggfantasy',
    packages=['ggfantasy'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'requests>=2.20.0',
        'crontab',
        'python-socketio>=3.0',
        'SQLAlchemy',
        'mysqlclient',
    ]
)