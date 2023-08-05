from setuptools import find_packages, setup


setup(
    name='deraser',
    version='0.0.1',
    description='Deep Learning Model Compression Based on Weight Pruning',
    long_description='',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='MIT',
    author='Anonymous',
    author_email='dwk@etri.re.kr',
    install_requires=['numpy'],
    keywords=['deep learning', 'model compression', 'weight pruning'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ]
)
