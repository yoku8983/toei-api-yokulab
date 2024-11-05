import os
import requests
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# Streamlit Webアプリの設定
st.set_page_config(layout="wide")  # widemodeで表示

# Streamlit Webアプリのタイトルを設定
st.title("都営新宿線  走行位置")

# アクセストークンを取得
access_token = os.getenv("ODPT_API_KEY")

# 日本語変換用のJSONファイルを読み込む
## 駅名
with open("Station_conv.json", "r", encoding="utf-8") as f:
    trans_station = json.load(f)

## 路線名、事業者名、方向
with open("RouteOperatorDirection.json", "r", encoding="utf-8") as f:
    trans_dirope = json.load(f)

## 列車種別
with open("odpt.json", "r", encoding="utf-8") as f:
    trans_odpt = json.load(f)

## 駅名
with open("stationlist.json", "r", encoding="utf-8") as f:
    trans_stalist = json.load(f)

# APIエンドポイントとパラメータ
url = "https://api.odpt.org/api/v4/odpt:Train"
params = {
    "odpt:operator": "odpt.Operator:Toei",
    "acl:consumerKey": access_token
}

# POSTリクエストの送信
response = requests.get(url, params=params)

filtered_data = []

# レスポンスボディの処理
if response.status_code == 200:
    # JSON形式のレスポンスを辞書として取得
    data = response.json()

    # 条件に一致するデータを抽出
    for item in data:
        if item.get("odpt:railway") == "odpt.Railway:Toei.Shinjuku":
            filtered_data.append({
#               "路線": trans_dirope.get(item.get("odpt:railway").split(".")[-1], item.get("odpt:railway")),
                "方向": trans_dirope.get(item.get("odpt:railDirection").split(":")[-1], item.get("odpt:railDirection")),
                "列車番号": item.get("odpt:trainNumber"),
                "車両": trans_dirope.get(item.get("odpt:trainOwner").split(":")[-1], item.get("odpt:trainOwner")),
                "種別": trans_odpt.get(item.get("odpt:trainType").split(".")[-1], item.get("odpt:trainType")),
                "終着駅": ", ".join(
                    [trans_station.get(station.split(".")[-1], station) for station in item.get("odpt:destinationStation", [])]
                ),
                "現在駅": trans_stalist.get(item.get("odpt:fromStation").split(".")[-1], item.get("odpt:fromStation")),
                "次駅": trans_stalist.get(item.get("odpt:toStation", "").split(".")[-1], "") if item.get("odpt:toStation") is not None else "",
                "遅延時間(分)": item.get("odpt:delay") // 60 if item.get("odpt:delay") is not None else None
            })

    # フィルタリングされたデータをデータフレームに変換
    df = pd.DataFrame(filtered_data)

    # 遅延時間がNoneでない行のみを表示
    df = df.dropna(subset=["遅延時間(分)"])

    # 遅延時間が20分以上の場合に色を付けるためのスタイル設定
    def highlight_delay(val):
        if isinstance(val, (int, float)) and val >= 20:
            return "background-color: LightPink; color: Red;"
        return ""

    # タイトル行のスタイルと遅延時間の条件付きスタイルを適用
    styled_df = df.style.applymap(highlight_delay, subset=["遅延時間(分)"])\
        .set_table_styles([
            {'selector': 'thead th', 'props': [('color', 'white'), ('background-color', 'DarkSlateBlue')]}
        ])

    # データフレームをStreamlitで表形式に表示
    st.write("公共交通オープンデータセンターのデータセットを利用しています。")
    st.write(styled_df.to_html(), unsafe_allow_html=True)

    # フィルタ結果をインデント付きで整形して表示
#    print("Filtered Data:", json.dumps(filtered_data, indent=2, ensure_ascii=False))

else:
    # エラーメッセージを表示
    st.error(f"Error {response.status_code}: {response.text}")

#else:
#    print(f"Error {response.status_code}: {response.text}")

