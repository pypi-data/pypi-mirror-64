import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='multissh',
    version='0.1.5',
    author='Jaan Porkon',
    author_email='jaantrill@gmail.com',
    description='Tool to connect to multiple SSH servers and broadcast commands.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JaanPorkon/MultiSSH',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'paramiko', 'tldextract'],
    scripts=['bin/mssh']
)