from setuptools import setup, find_packages

setup(
    name='zphishing-apex',
    version='4.0.0',
    description='The Most Advanced Phishing Framework Ever Created',
    author='worm shadow',
    author_email='wormshadow@example.com',
    url='https://github.com/wormshadow/zphishing-apex',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=3.0.0',
        'flask-socketio>=5.3.6',
        'flask-sqlalchemy>=3.1.1',
        'flask-jwt-extended>=4.6.0',
        'click>=8.1.7',
        'rich>=13.7.0',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'zphishing=zphishing:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
