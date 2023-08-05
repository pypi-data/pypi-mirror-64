from setuptools import setup

version = '0.0.1'
name = 'openbd'
short_description = '`openbd` is a package for openBD( https://openbd.jp/ ).'
long_description = """\
`openbd` is a package for openBD.
::

   from openbd import book_info
   print(book_info('4764905809'))
   >>>
   BookInfo(isbn='9784764905801', title='データ分析ライブラリーを用いた最適化モデルの作り方',
   subtitle=None, series='Pythonによる 問題解決シリーズ', authors='斉藤 努／著、久保 幹雄／監修',
   publish='近代科学社', date='2018/12/13', price='3200円', page='224', size='B5変形',
   content='各種ライブラリを組み合わせることで、シンプルで分かりやすい最適化モデルの作成方法を学ぶ',
   image='https://cover.openbd.jp/9784764905801.jpg', data=None)

Requirements
------------
* Python 3

Features
--------
* nothing

Setup
-----
::

   $ pip install openbd

History
-------
0.0.1 (2020-3-23)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
   "Topic :: Scientific/Engineering",
]  # noqa

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    py_modules=['openbd'],
    keywords=['openbd', ],
    author='Saito Tsutomu',
    author_email='tsutomu.saito@beproud.jp',
    url='https://pypi.python.org/pypi/openbd',
    license='PSFL',
    entry_points={'console_scripts': ['openbd = openbd:main']},
)
