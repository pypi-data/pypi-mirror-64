from setuptools import setup, find_packages

long_description = "simple api for monitoring of loadaverage.ir"


setup (
    name = 'loadavgapi',
    version = '1.1.1',
    description = 'API DEVELOPMENT FOR LOADAVG',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license='MIT',
    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            'loadavg = src.loadavg:main'
        ]
    },

    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent", 
    ),

    keywords = 'python',
    install_requires = [
        "flask",
        "psutil",
    ],
    zip_safe = False
)
