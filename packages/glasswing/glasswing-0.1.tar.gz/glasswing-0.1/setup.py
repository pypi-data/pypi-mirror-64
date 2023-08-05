import setuptools


setuptools.setup(
    name='glasswing',
    version='0.1',
    author='Jessy Lauer',
    author_email='jlauer@rowland.harvard.edu',
    description='GlassWing is a library for nonlinear dynamics analysis in Python.',
    url='https://github.com/jeylau/glasswing',
    license='BSD 3-clause "New" or "Revised License"',
    long_description='',
    install_requires=[
        'numpy>=1.14.0',
        'scipy>=1.1.0',
        'matplotlib>=3.0.0',
    ],
    python_requires='>=3.6',
    packages=[],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
)
