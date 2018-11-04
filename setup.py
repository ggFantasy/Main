from setuptools import setup

setup(
    name='ggfantasy',
    packages=['ggfantasy'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests>=2.20.0',
        'crontab',
    ]
)