from distutils.core import setup

setup(
    name='hfh',
    version='0.2',
    author='eoglethorpe',
    author_email='ewanogle@gmail.com',
    description='Scripts for Habitat for Humanity Nepal EQ Reconstruction',
    packages=['hfh'],
    install_requires=[
        'sqlalchemy',
        'overpass',
        'click',
        'qrcode'
    ],
)
