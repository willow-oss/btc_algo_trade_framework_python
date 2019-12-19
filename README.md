# btc_algo_trade_framework_python

## Overview
BTCの自動売買用のプログラムです。

## Contents
websocket_exchange - 各取引所（bitFlyer、BitMex）から約定履歴、板情報をwebsocketで購読し、mySQLデータベースに格納するモジュールです。

create_features - mySQLDBの情報を加工し、モデルが使用する特徴量を作るモジュールです。公開するかは未定です。現状では、この特徴量の内一部をサンプルとしてcsvファイルでおいておくことを考えています。

model - 特徴量から、期待リターン・スプレッド（ボラ）を計算するモジュールです。

bot - modelから期待リターンとボラを受け取り、取引所に対して発注等のアクションを起こすmoduleです。
