import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aiogram_datepicker',
    packages=setuptools.find_packages(),
    version='0.0.8',
    license='MIT',
    description='Telegram Bots datepicker & Aiogram datepicker',
    author='Briler',
    author_email='netbriler@gmail.com',
    url='https://github.com/netbriler/aiogram-datepicker',
    download_url='https://github.com/netbriler/aiogram-datepicker/archive/refs/tags/0.0.8.tar.gz',
    keywords=['Aiogram', 'Telegram', 'Bots', 'Calendar', 'Datepicker'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'aiogram'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.9',
)
