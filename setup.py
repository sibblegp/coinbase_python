from distutils.core import setup

setup(
    name='subtledata',
    version='0.0.4',
    packages=['subtledata', 'subtledata.api', 'subtledata.api.models'],
    url='http://dev.subtledata.com/libraries/python',
    license='MIT',
    author='George Sibble',
    author_email='george.sibble@subtledata.com',
    description='Integration Library for the Subtledata Platform',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
