
import setuptools


with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sainofirst',
    version='1.0.1',
    author="Sainofirst",
    author_email = 'contact@sainofirst.com',
    maintainer='Shubz Kothekar',
    maintainer_email='hello@shubzkothekar.com',
    description="The Sainofirst SDK for python provides a python API for Sainofirst communication services.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sainofirst/sainofirst-sdk-python",
    package_dir={'': 'src'},
    packages=['sainofirst', 'sainofirst.services.sms', 'sainofirst.services.voice'],
    keywords='sdk bulk-sms bulk-voice sms-gateway voice-call',
    install_requires=[
        'requests>=2'
    ],
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: Apache Software License'
    ],
    python_requires='>=3',
    package_data={  
        'sainofirst': ['config.json', 'errors.json', 'services'],
    },
    include_package_data=True,
    project_urls={   
        'documentation' : 'https://sainofirst.github.io/sainofirst-sdk-python', 
        'website': 'https://www.sainofirst.com',
        'source' : "https://github.com/sainofirst/sainofirst-sdk-python"
    },
    zip_safe=False
 )