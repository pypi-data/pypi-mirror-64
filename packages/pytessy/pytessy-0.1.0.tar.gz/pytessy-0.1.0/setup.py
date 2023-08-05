import setuptools

with open('README.md', 'r') as instream:
    long_description = instream.read()

setuptools.setup(
    name = 'pytessy',
    version = '0.1.0',
    author = 'rixel',
    author_email = 'python@hyperrixel.com',
    description = 'Tesseract-OCR, faster',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/hyperrixel/pytessy',
    keywords = 'tesseract Tesseract-OCR',
    project_urls = {'Documentation' : 'https://pytessy.readthedocs.io/',
                    'Source' : 'https://github.com/hyperrixel/pytessy',
                    'Projects' : 'https://hyperrixel.github.io/',
                    'Homepage' : 'https://www.hyperrixel.com/'},
    packages=setuptools.find_packages(),
    classifiers = ['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
                   'Operating System :: OS Independent'],
    python_requires = '>=3.6',
)
