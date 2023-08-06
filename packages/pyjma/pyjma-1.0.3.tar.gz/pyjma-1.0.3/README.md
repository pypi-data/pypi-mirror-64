# PyJMA - 日本気象庁災害データ抽出ライブラリ

## 機能紹介

PyJMA は[日本気象庁](https://www.jma.go.jp/jma/index.html)から公開した[気象・災害データ](https://www.data.jma.go.jp/developer/index.html)を抽出するための Python ライブラリです。

主要機能：
- 地震データの抽出

Todo:
- 台風データの抽出
- 火山データの抽出

## 利用開始

- pip でのインストール（おすすめ）

```
$ pip install pyjam
```

- ソースからインストール

```
$ git clone https://github.com/liaocyintl/pyjma
$ cd pyjam
$ python setup.py install
```

## 利用方法

- 災害データ取得
data_typesで取得するデータタイプを指定します。
```python
import pyjma as pg
data_types = ["earthquake"]
data = pg.disaster_data(data_types)
```

- 取得可能のデータタイプ
  - earthquake : 地震


- 取得したデータ
```json
{
    'status': 'OK',
    'results': [{
        // 地震情報
        'type': 'earthquake',
        // データ識別し
        'uuid': 'urn:uuid:a8c35460-1b3e-3f99-ad8a-053ae2a2006f',
        // データリンク
        'link': 'http://www.data.jma.go.jp/developer/xml/data/a8c35460-1b3e-3f99-ad8a-053ae2a2006f.xml',
        // 震強
        'magnitude': 4.1,
        // 震央緯度経度
        'location': {'lon': 140.4, 'lat': 35.4},
        // 深さ
        'depth': 30000,
        // 発生日時
        'origin_time': datetime.datetime(2020, 3, 30, 17, 15, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))),
        // 震央
        'epicenter': '千葉県東方沖',
        // コメント
        'comment': 'この地震による津波の心配はありません。'
    }]
}
```

## 更新履歴

- 1.0.0
  - 地震情報の取得
  - ライブラリ初期化
