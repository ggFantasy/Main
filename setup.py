from setuptools import setup

setup(
    name='ggfantasy',
    packages=['ggfantasy'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'crontab',
    ]
)