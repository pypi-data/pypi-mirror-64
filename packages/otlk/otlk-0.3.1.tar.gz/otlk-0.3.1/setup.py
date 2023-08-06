# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['otlk']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'pyyaml>=5.3,<6.0',
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.6,<0.9.0',
 'tqdm>=4.42.0,<5.0.0']

entry_points = \
{'console_scripts': ['otlk = otlk.main:main']}

setup_kwargs = {
    'name': 'otlk',
    'version': '0.3.1',
    'description': 'outlookの情報を取得するためのCLIツール',
    'long_description': '# 概要\nMicrosoft Outlook上のデータを取得するためのCLIツールです\n\n# 機能\n```\n$ otlk --help\n\nUsage: otlk [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  empty   対象ユーザー同士での共通した空き時間を取得\n  event   対象ユーザーのイベントを取得\n  me      自身のユーザー情報を表示\n  people  ユーザー一覧をを表示\n```\n\n- 細かなオプションは、それぞれのコマンドの`--help`で確認のこと\n\n## 自分のアカウントを確認\n\n```\n$ otlk me\n\n|                | me                                   |\n|:---------------|:-------------------------------------|\n| id             | xxxx                                 |\n| displayName    | hase hiro                            |\n| user_id        | me                                   |\n| mobilePhone    |                                      |\n| officeLocation |                                      |\n| mobilePhone    |                                      |\n```\n\n## 所属するグループのユーザーを確認\n```\n$ otlk people\n\n|     | displayName                                                       | user_id                            | companyName      |\n|----:|:------------------------------------------------------------------|:-----------------------------------|:-----------------|\n|   0 | xxxx                                                              | xxx@exapmle.com                    |                  |\n|   1 | yyyy                                                              | yyy@example.com                    | ABC              |\n|   2 | zzzz                                                              |                                    |                  |\n```\n\n## 予定一覧を確認\n```\n$ otlk [ユーザー名]  --start [YYYY/mm/dd HH/MM] --end [YYYY/mm/dd HH/MM] \n\n|    | subject                                                                                  | locations            | start.dateTime      | end.dateTime        |\n|---:|:-----------------------------------------------------------------------------------------|:---------------------|:--------------------|:--------------------|\n|  0 | subjectA                                                                                 | []                   | 2020-03-02 18:00:00 | 2020-03-02 18:30:00 |\n|  1 | subjectB                                                                                 | []                   | 2020-03-02 19:00:00 | 2020-03-02 20:00:00 |\n...\n```\n- `-d`オブションをつけることで、参加者一覧や、終日の予定かどうかなどの、付属情報も確認可能\n- ユーザー名を省略した場合、自身の予定が出力される\n- `--start[end]`の時間以下は省略可能。また、それぞれのオプションを省略した場合、直近の予定が出力される\n\n## 指定したユーザー同士の空いている時間を確認\n```\n$ otlk empty [ユーザー名1] [ユーザー名2]  ... --minutes [確保したい時間(分) --start [YYYY/mm/dd HH/MM] --end [YYYY/mm/dd HH/MM] \n\n|    | from             | to               |\n|---:|:-----------------|:-----------------|\n|  0 | 2020/03/29 18:45 | 2020/03/30 10:00 |\n|  1 | 2020/03/30 13:00 | 2020/03/30 13:30 |\n|  2 | 2020/03/30 13:45 | 2020/03/30 16:00 |\n|  3 | 2020/03/30 17:30 | 2020/03/30 18:00 |\n```\n\n- `--start[end]`の時間以下は省略可能。また、それぞれのオプションを省略した場合、直近数日の予定が出力される\n\n\n# 設定方法\n## インストール\n```\npip install -U otlk\n```\n\n## 認証\n- [公式のアプリケーションの認証方法](https://docs.microsoft.com/ja-jp/outlook/rest/get-started)に従い、アプリケーションを登録し、`client_id`, `client_secret`および、`refresh_token`を取得\n- 発行時のスコープには以下を含める\n```\n[\n    "openid",\n    "offline_access",\n    "User.Read",\n    "Calendars.Read",\n    "Calendars.Read.Shared",\n    "People.Read"\n]\n```\n\n## credential.jsonを作成\n上記の情報から、json形式のファイルを作成する\n```\n{\n"client_id": "xxxx",\n"client_secret": "yyyy",\n"refresh_token": "zzzz"\n\n}\n```\n\n## 環境変数の設定\n上記の`credential.json`のPATHを、以下の環境変数に設定\n```\n export OTLK_CREDENTIAL="[path]/[to]/credential.json"\n```\n\n## 確認\n下記のコマンドで、自身の情報が返ってくれば成功\n```\notlk me\n```\n',
    'author': 'Hiroaki Hasegawa',
    'author_email': 'hasepappa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
