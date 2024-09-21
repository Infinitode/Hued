from setuptools import setup, find_packages

setup(
    name='hued',
    version='{{VERSION_PLACEHOLDER}}',
    author='Infinitode Pty Ltd',
    author_email='infinitode.ltd@gmail.com',
    description='An open-source Python library for color generation, conversion and retrieval of common properties, palettes, and color information.',
    long_description='An open-source Python library for color processing, random color generation, conversion between common types, and retrieval of common color properties, color palettes, and color information.',
    long_description_content_type='text/markdown',
    url='https://github.com/infinitode/deepdefend',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
)