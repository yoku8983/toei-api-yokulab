# toei-api-yokulab

## 概要
都営新宿線のリアルタイム在線位置情報のAPIを叩き、表形式でWEBブラウザ上で表示できるようにしたアプリです。
[公共交通オープンデータセンター](https://www.odpt.org/)のAPIを使用しています。
Azure App Servicesを利用してホスティングしています。FREEプランなのでアクセス量規制あり。
[https://toei-shinjuku-location-hrdrcwh7ekf7hpbf.canadacentral-01.azurewebsites.net/](https://toei-shinjuku-location-hrdrcwh7ekf7hpbf.canadacentral-01.azurewebsites.net/)

## 表示可能な情報
終車後など在線がない場合は、その旨が表示されます。
- **方向**：東行き（本八幡行き）/西行き（新宿行き）
- **列車番号**：末尾Tは都営車、末尾Kは京王車の運用です。
- **車両**：都営車/京王車。列番の末尾と異なる場合は代走です。
- **種別**：都営線内種別を表示します。京王線内種別の表示には対応しておりません。
- **終着駅**：終点の駅
- **現在駅**：停車時は停車中の駅、駅間走行中は発車済の駅を表します。
- **次駅**：駅間走行中は、次の停車駅・通過駅を表します。駅停車中は無表示です。
- **遅延時分（分）**：何分遅延しているかを表示します。20分以上遅延している列車は、遅延時分のセルが赤背景になります。

## `src/`配下 各コードの解説

### `toeisub_location.py`
メイン処理を記述したPythonコードです。APIを叩き、取得したレスポンスボディをパースします。
その後StreamlitとPandasを利用して表形式の整形と、WEBサイト表示を実現しています。
- APIキー`ODPT_API_KEY`はAzure App Services側で環境変数を設定しています。
ローカルで実行する場合は環境変数を設定するか、`.env`に記述してください。本スクリプト中の`.env`読み込み部分のコードもコメントアウト解除すること。
- 行先や現在位置の駅名、路線名などは全てローマ字なので、自作したJSONファイル群を使用して日本語表記に変換しています。

### `Station_conv.json`
終着駅のローマ字・日本語表記変換用のデータセットです。乗入れ先の駅名も記載されています。

### `stationlist.json`
現在駅・次駅のローマ字・日本語表記変換用のデータセットです。都営地下鉄の全駅名が記載されています。乗入れ先の事業者の駅名は入ってません。

### `RouteOpratorDirection.json`
車両の所属と行先方向のローマ字・日本語表記変換用のデータセットです。

### `odpt.json`
列車種別のローマ字・日本語表記変換用のデータセットです。都営地下鉄の全種別が格納されています。
