import setuptools

with open('./README.md') as f:
    README = f.read()

setuptools.setup(
    author="Mark7888",
    author_email="l.mark7888@gmail.com",
    name='tf2calc',
    license="MIT",
    description='python package to calculate tf2 prices',
    version='v1.0.0',
    long_description_content_type='text/markdown',
    long_description=README,
    url='https://github.com/Mark7888/tf2clac',
    packages=setuptools.find_packages(),
    python_requires=">=3",
    install_requires=['requests', 'pricestf'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
