# MELSEC iQ-R MES Interface Module

仕様を理解してトラブル時のデバッグ/工数削減ツール作成を目指します

# 目次
1. 機能
    - MESインタフェースユニットの動作
    - アクション実行タイミングとアクションの種類
    - ジョブ構成の種類
    - ジョブ動作時のCPUユニットへのデータの読み書きタイミング
    - ジョブの動作
    - トリガ判定時のアクセス種別
2. 情報連携機能設定ツール
    - ファイル構成
    - プロジェクト構造
3. mes_parser
    - 使い方
    - JSON仕様
    - CSV -> JSON
        - PROJECT.CSV
        - JOB.CSV
        - JOB_NOTICE.CSV
        - TRIGGER_CONDITION.CSV
        - DB_ASSIGNMENT.CSV
        - DB_COMMUNICATION.CSV
        - DB_NARROWING_DOWN.CSV
        - DB_SORTING_ORDER.CSV
        - TARGET_DEVICE.CSV
        - DEVICE_TAG.CSV
        - DEVICE_TAG_COMPONENT.CSV
        - TARGET_SERVER.CSV
        - ACCESS_TABLE.CSV
        - ACCESS_FIELD.CSV
        - NETWORK.CSV
        - LOCAL_VARIABLE.CSV
        - GLOBAL_VARIABLE.CSV
        - DB_BUFFER.CSV
        - SECURITY.CSV
        - DOT_MATRIX_LED.CSV
        - USER.CSV
    
# 1. 機能

MESインタフェースユニットの機能詳細について説明します。

## MESインタフェースユニットの動作

MESインタフェースユニットは，下記設定に基づいて動作することで情報連携を実現します。  

<img src="data\img\2024-04-08 145514.png">

MESインタフェースユニットは，情報連携機能がジョブ設定のトリガ条件を監視し，条件成立時にジョブ設定のアクションを順次実行し，CPUユニットとデータベースのデータ連携を実現します。  
情報連携機能は，CPUユニットのデバイスデータを入出力するためにデータ入出力機能を使用し，デバイスタグ要素としてデータの読出し/書込みを行います。  
その際にデータ入出力機能はアクセスするCPUユニットをアクセス先機器設定で特定します。  
また，情報連携機能は，データベースとのアクセスを行うためにデータ入出力機能を使用し，アクセステーブル/プロシージャとしてアクセスします。  
その際にデータ入出力機能はアクセスするサーバをアクセス先サーバ設定で特定します。  

<img src="data\img\2024-04-08 141325.png">

## アクション実行タイミングとアクションの種類

ジョブ設定のアクションに指定できるアクションの種類は，下記の3通りがあります。

<img src="data\img\2024-04-08 151937.png">

ジョブ設定のアクションの設定は，基本的には一連の処理をまとめて指定します(基本構成)。  
また，その実行タイミングと用途に応じて前処理，メイン処理，後処理に分けて指定することもできます(拡張構成)。  
それぞれのタイミングに指定可能なアクション種別は下記のとおりです。  
○: 指定可，×: 指定不可  

<img src="data\img\2024-04-08 152020.png">

## ジョブ構成の種類

ジョブの構成には基本構成，拡張構成の2種類があり，アクションの指定可否が異なります。  
○: 指定可，×: 指定不可  

<img src="data\img\2024-04-08 152101.png">

## ジョブ動作時のCPUユニットへのデータの読み書きタイミング

情報連携機能がジョブを動作させるために，下記タイミングでデータ入出力機能を使用してCPUユニットへデータの読み書きを実施します。  
情報連携機能はアクションを実行する際に事前に必要なCPUユニットのデータを準備します。  
アクション実行中はCPUユニットへデータの読み書きを行わず，アクション実行後にまとめてCPUユニットへデータを書き込みます。  

<img src="data\img\2024-04-08 152133.png">

ただし，トリガ判定時のデータとアクションが使用するデータとで，データの同期が必要な場合(同一タイミングのデータである必要がある場合)のために，アクションが使用するデータもトリガ判定時に収集させることもできます。  
アクションが使用するデータもトリガ判定時に収集させることで，1回のジョブ実行で扱うCPUユニットのデータを同一のタイミングのデータに統一できます。  

<img src="data\img\2024-04-08 152201.png">

## ジョブの動作

ジョブは，ジョブを構成する各処理(前処理/メイン処理/後処理)の実行結果と，各処理を構成するアクションの実行結果によって動作します。  

<img src="data\img\2024-04-08 152330.png">

- 処理の実行結果

処理(前処理/メイン処理/後処理)の実行結果の状態を表します。  
実行結果の種類ごとに，処理の流れの制御，および実行結果の通知が可能です。  

<img src="data\img\2024-04-08 152400.png">

- アクションの実行結果

各アクションの実行結果の状態を表します。  

<img src="data\img\2024-04-08 152430.png">

- 失敗/中断時の動作仕様

<img src="data\img\2024-04-08 152509.png">

- 例外共通動作仕様

<img src="data\img\2024-04-08 152537.png">

## トリガ判定時のアクセス種別

トリガ判定にCPUユニットなどの機器の値を監視する場合，情報連携機能はデバイスメモリ入出力機能を使用してデータを読み出します。    

<img src="data\img\2024-04-08 152611.png">

# 2. 情報連携機能設定ツール

情報連携機能設定ツールは，MESインタフェースユニットを動作させるために必要な各種設定を，MESインタフェースユニットに設定するツールです。  
MESインタフェースユニットの各ステータス，稼動ログの確認や，MESインタフェースユニットの停止，再開の各種操作を行うことができます。  
情報連携機能設定ツールは，MESインタフェースユニット1台分の情報連携機能の設定を1つのプロジェクトとして扱います。  

- [MELSEC iQ-R MESインタフェースユニットユーザーズマニュアル(スタートアップ編).pdf](https://github.com/taaaakeeen/MELSEC_iQ-R_MES_Interface_Module/blob/main/doc/MELSEC%20iQ-R%20MES%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%95%E3%82%A7%E3%83%BC%E3%82%B9%E3%83%A6%E3%83%8B%E3%83%83%E3%83%88%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%BA%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB(%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88%E3%82%A2%E3%83%83%E3%83%97%E7%B7%A8).pdf)

- [MELSEC iQ-R MESインタフェースユニットユーザーズマニュアル(応用編).pdf](https://github.com/taaaakeeen/MELSEC_iQ-R_MES_Interface_Module/blob/main/doc/MELSEC%20iQ-R%20MES%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%95%E3%82%A7%E3%83%BC%E3%82%B9%E3%83%A6%E3%83%8B%E3%83%83%E3%83%88%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%BA%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB(%E5%BF%9C%E7%94%A8%E7%B7%A8).pdf)

## ファイル構成
以下のCSVファイルによって設定が構成されています

### プロジェクト設定
- PROJECT.CSV
### ジョブ設定
- JOB.CSV
- JOB_NOTICE.CSV
- TRIGGER_CONDITION.CSV
### アクション設定
- DB_ASSIGNMENT.CSV
- DB_COMMUNICATION.CSV
- DB_NARROWING_DOWN.CSV
- DB_SORTING_ORDER.CSV
### アクセス先機器設定
- TARGET_DEVICE.CSV
### デバイスタグ設定
- DEVICE_TAG.CSV
- DEVICE_TAG_COMPONENT.CSV
### アクセス先サーバ設定
- TARGET_SERVER.CSV
### アクセステーブル/プロシージャ設定
- ACCESS_TABLE.CSV
- ACCESS_FIELD.CSV
### ネットワーク設定
- NETWORK.CSV
### オプション設定
- LOCAL_VARIABLE.CSV
- GLOBAL_VARIABLE.CSV
- DB_BUFFER.CSV
- SECURITY.CSV
- DOT_MATRIX_LED.CSV
- USER.CSV

## プロジェクト構造
以下のディレクトリ構造で構成されています

```
project
|- PROJECT.CSV
|- JOB.CSV
|- JOB
|   |- JOB_NOTICE.CSV
|   |- TRIGGER_CONDITION.CSV
|   |- ACTION
|       |- DB_ASSIGNMENT.CSV
|       |- DB_COMMUNICATION.CSV
|       |- DB_NARROWING_DOWN.CSV
|       |- B_SORTING_ORDER.CSV
|- TARGET_DEVICE.CSV
|- DEVICE_TAG.CSV
|- DEVICE_TAG_COMPONENT.CSV
|- TARGET_SERVER.CSV
|- ACCESS_TABLE.CSV
|- NETWORK.CSV
|- LOCAL_VARIABLE.CSV
|- GLOBAL_VARIABLE.CSV
|- DB_BUFFER.CSV
|- SECURITY.CSV
|- DOT_MATRIX_LED.CSV
|- DOT_MATRIX_LED.CSV
|- USER.CSV
```

# 3. mes_parser
CSVのプロジェクトファイルをJSONに変換出力します。  
トラブル等でMES側の設定を確認したい状況での使用を想定しています。

[mes_parser.exe](https://github.com/taaaakeeen/MELSEC_iQ-R_MES_Interface_Module/blob/main/dist/mes_parser.exe)

## 使い方

1. mes_parser.exeを実行

<img src="data\img\2024-04-08 162559.png">

2. GUIが起動します

<img src="data\img\2024-04-08 163639.png">

3. フォルダ選択でプロジェクトフォルダを選択します

<img src="data\img\2024-04-08 164001.png">

4. 選択したフォルダのパスがテキストボックスに入力されます ※ダイアログを使用せずに直接入力でもOK

<img src="data\img\2024-04-08 164052.png">

5. JSON出力ボタンを押すと実行確認のモーダルが表示されます

<img src="data\img\2024-04-08 164528.png">

6. 処理が完了すると処理完了のモーダルが表示されます

<img src="data\img\2024-04-08 164728.png">

### 出力ファイルの確認

1. mes_parser.exeと同じ階層にoutputフォルダが作成されます

<img src="data\img\2024-04-08 165314.png">

2. outputフォルダにプロジェクトフォルダ名のJSONが出力されます

<img src="data\img\2024-04-08 165650.png">

### 変換失敗

1. 処理中にエラーが発生すると変換失敗のモーダルが表示されます

<img src="data\img\2024-04-08 170007.png">

2. mes_parser.exeと同じ階層にmes_parser.logが作成されます

<img src="data\img\2024-04-08 170311.png">

3. エラー内容を確認できます

<img src="data\img\2024-04-08 170623.png">

## JSON仕様
以下のKey構造で構成されています

```
{
    "PROJECT": {
        "PROJECT_NAME": "",
        "COMMENT": "",
        "CSV_FORMAT_VERSION": ""
    },
    "NETWORK": {
        "CH1": {
            "USE_CH1": "",
            "IP_ADDRESS": "",
            "SUBNET_MASK": ""
        },
        "CH2": {
            "USE_CH2": "",
            "IP_ADDRESS": "",
            "SUBNET_MASK": ""
        },
        "DEFAULT_GATEWAY": "",
        "HOST_NAME": ""
    },
    "TARGET_DEVICE": [
        {
            "TARGET_DEVICE_NUM": "",
            "TARGET_DEVICE_NAME": "",
            "COMMENT": "",
            "DEVICE_TYPE": "",
            "MULTIPLE_CPU": "",
            "SINGLE_NETWORK": "",
            "SOURCE_MODULE_TYPE": "",
            "SOURCE_ROUTE": "",
            "SOURCE_START_IO_NUM": "",
            "SOURCE_STATION_NUM": "",
            "ROUTED_IP_ADDRESS": "",
            "ROUTED_MODULE_TYPE": "",
            "ROUTED_NETWORK_NUM": "",
            "ROUTED_STATION_NUM": "",
            "TARGET_MODULE_TYPE": "",
            "TARGET_IP_ADDRESS": "",
            "TARGET_NETWORK_NUM": "",
            "TARGET_STATION_NUM": "",
            "DIFFERENT_NETWORK": "",
            "RELAY_MODULE_TYPE": "",
            "RELAY_START_IO_NUM": "",
            "CO-EX_NETWORK_NUM": "",
            "CO-EX_STATION_NUM": "",
            "GLOBAL_LABEL_SETTING": "",
            "GLOBAL_LABEL_PATH_SETTING": ""
        }
    ],
    "DEVICE_TAG": [
        {
            "TAG_NUM": "",
            "TAG_NAME": "",
            "COMMENT": "",
            "PROTECT_DATA_WRITING": "",
            "ARRAY_TAG_SETTING": "",
            "ARRAY_SIZE": "",
            "ARRAY_TYPE": "",
            "SPECIFY_BLOCK_SIZE": "",
            "ARRAY_BLOCK_SIZE": ""
        }
    ],
    "DEVICE_TAG_COMPONENT": [
        [
            {
                "TAG_NUM": "",
                "COMPONENT_NUM": "",
                "COMPONENT_NAME": "",
                "TARGET_DEVICE_NUM": "",
                "DEVICE_MEMORY": "",
                "DATA_TYPE": "",
                "LENGTH": "",
                "GLOBAL_LABEL": ""
            }
        ]
    ],
    "TARGET_SERVER": [
        {
            "TARGET_SERVER_NUM": "",
            "TARGET_SERVER_NAME": "",
            "COMMENT": "",
            "SERVER_TYPE": "",
            "ACCESS_TYPE": "",
            "IP_ADDRESS": "",
            "PORT_NUM": "",
            "COMMUNICATION_TIMEOUT": "",
            "DB_ACCESS_TIMEOUT": "",
            "DATA_SOURCE_NAME": "",
            "USER_NAME": "",
            "PASSWORD": "",
            "DATABASE_TYPE": "",
            "NOTIFY_ACCESS_ERROR": "",
            "NOTICE_DST": ""
        }
    ],
    "ACCCESS_TABLE": [
        {
            "ACCESS_TABLE_NUM": "",
            "ACCESS_TABLE_NAME": "",
            "COMMENT": "",
            "TARGET_SERVER_NUM": "",
            "TABLE_PROC_TYPE": "",
            "DB_TABLE_NAME": ""
        }
    ],
    "ACCCESS_FIELD": [
        [
            {
                "ACCESS_TABLE_NUM": "",
                "ACCESS_FIELD_NUM": "",
                "ACCESS_FIELD_NAME": "",
                "DB_FIELD_NAME": "",
                "DATA_TYPE": "",
                "PRECISION_HOLD": "",
                "DEFAULT_VALUE_SETTING": "",
                "DEFAULT_VALUE": "",
                "DIRECTION": ""
            }
        ]
    ],
    "JOB": [
        {
            "JOB_NUM": "",
            "JOB_NAME": "",
            "COMMENT": "",
            "JOB_CONFIGURATION": "",
            "PRE_ACTION_NUM": "",
            "POST_ACTION_NUM": "",
            "TRIGGER_CONFIGURATION": "",
            "TRIGGER_COMBINATION": "",
            "TRIGGER_BUFFERING": "",
            "ACCESS_TYPE": "",
            "ACCESS_INTERVAL": "",
            "ACCESS_INTERVAL_UNIT": "",
            "READING_TARGET": "",
            "PRE_FAIL_OPERATION": "",
            "MAIN_FAIL_OPERATION": "",
            "MAIN_ABORT_OPERATION": "",
            "DB_BUFFERING_SETTING": "",
            "DB_BUFFERING_OPERATION": "",
            "WORKING_HISTORY": "",
            "DETAILED_LOG": "",
            "INHIBIT_OUTPUT_DEVICE": "",
            "INHIBIT_OUTPUT_SERVER": "",
            "INHIBIT_JOB_EXECUTION": "",
            "TRIGGER_CONDITION": [
                {
                    "TRIGGER_NUM": "",
                    "EVENT_CONDITION_TYPE": "",
                    "DETAIL_TYPE": "",
                    "MONITORING_TARGET": "",
                    "CONDITION": "",
                    "COMPARISON_TARGET": "",
                    "MONTH": "",
                    "DAY": "",
                    "WEEK": "",
                    "MON-SUN": "",
                    "START_TIME": "",
                    "END_TIME": "",
                    "TIMER_INTERVAL": "",
                    "TIME_INTERVAL": "",
                    "TIME_INTERVAL_UNIT": "",
                    "REFERENCE_TIME": "",
                    "MESIF_MODULE_STARTUP": "",
                    "MESIF_FUNC_RESTART": "",
                    "CONTROL_CPU_STATUS": "",
                    "REQUEST_SRC": "",
                    "NOTICE_DST": "",
                    "REQUEST_SRC2": "",
                    "NOTICE_DST2": ""
                }
            ],
            "JOB_NOTICE": [
                {
                    "NOTICE_TYPE": "",
                    "NOTICE_SETTING": "",
                    "NOTICE_DST": "",
                    "NOTICE_DATA": ""
                }
            ],
            "ACTION": [
                {
                    "ACTION_NUM": "",
                    "DB_COMMUNICATION": [
                        {
                            "DB_COMMUNICATION_TYPE": "",
                            "ACCESS_TABLE_NUM": "",
                            "RECORD_NUM_NOTICE": "",
                            "RECORD_NUM_DST": "",
                            "SELECTED_RECORD_NUM_DST": "",
                            "SET_MAX_RECORD_NUM": "",
                            "MAX_RECORD_NUM": "",
                            "M-SELECT_ZERO_CLEAR": "",
                            "SET_DEFAULT_VALUE": "",
                            "RETURN_VALUE_NOTICE": "",
                            "RETURN_VALUE_DST": "",
                            "NO_RECORD_OPERATION": "",
                            "NO_RECORD_NOTICE": "",
                            "NO_RECORD_NOTICE_DST": "",
                            "NO_RECORD_NOTICE_DATA": "",
                            "NO_RECORD_ZERO_CLEAR": "",
                            "M-RECORDS_OPERATION": "",
                            "M-RECORDS_NOTICE": "",
                            "M-RECORDS_NOTICE_DST": "",
                            "M-RECORDS_NOTICE_DATA": "",
                            "OVERFLOW_OPERATION": "",
                            "OVERFLOW_NOTICE": "",
                            "OVERFLOW_NOTICE_DST": "",
                            "OVERFLOW_NOTICE_DATA": "",
                            "SELECT_FROM_FIRST": "",
                            "INSERT_NEW_RECORD": ""
                        }
                    ],
                    "DB_NARROWING_DOWN": [
                        {
                            "NARROWING_DOWN_NUM": "",
                            "COMBINATION": "",
                            "ACCESS_FIELD_NUM": "",
                            "CONDITION": "",
                            "COMPARISON_TARGET": ""
                        }
                    ],
                    "DB_SORTING_ORDER": [
                        {
                            "SORTING_ORDER_NUM": "",
                            "ACCESS_FIELD_NUM": "",
                            "ORDER": ""
                        }
                    ],
                    "DB_ASSIGNMENT": [
                        {
                            "ASSIGNMENT_NUM": "",
                            "ACCESS_FIELD_NUM": "",
                            "ASSIGNMENT_DATA": ""
                        }
                    ]
                }
            ]
        }
    ],
    "DB_BUFFER": [
        {
            "DB_BUFFER_NUM": "",
            "USE_DB_BUFFER": "",
            "DB_BUFFER_NAME": "",
            "DB_BUFFER_SIZE": "",
            "RESEND_AUTO": "",
            "OPERATION_RECOVERY": "",
            "RESEND_REQUEST": "",
            "CLEAR_REQUEST": "",
            "STATUS_NOTICE_DST": "",
            "NUM_NOTICE_DST": "",
            "FULL_NOTICE_DST": "",
            "USE_RATE_NOTICE_DST": ""
        }
    ],
    "DOT_MATRIX_LED": [
        {
            "DEFAULT_MODE": "",
            "SWITCH_FORCIBLY": "",
            "HIGHLIGHT_DISPLAY": ""
        }
    ],
    "GLOBAL_VARIABLE": [
        {
            "VARIABLE_NUM": ",
            "VARIABLE_NAME": "",
            "COMMENT": "",
            "DATA_TYPE": "",
            "LENGTH": ""
        }
    ],
    "LOCAL_VARIABLE": [
        {
            "VARIABLE_NUM": ",
            "VARIABLE_NAME": "",
            "COMMENT": "",
            "DATA_TYPE": "",
            "LENGTH": ""
        }
    ],
    "SECURITY": [
        {
            "USE_USER_AUTH": ""
        }
    ],
    "USER": [
        {
            "ACCOUNT_NUM": "",
            "USER_NAME": "",
            "PASSWORD": ""
        }
    ]
}

```

## CSV -> JSON
JSONの各KeyはCSVのファイル名になっています

## PROJECT.CSV

<img src="data\img\2024-04-08 140736.png">

## JOB.CSV

<img src="data\img\2024-04-08 160456.png">

## JOB_NOTICE.CSV

<img src="data\img\2024-04-08 160314.png">

## TRIGGER_CONDITION.CSV

<img src="data\img\2024-04-08 160131.png">

## DB_ASSIGNMENT.CSV

<img src="data\img\2024-04-08 155509.png">

## DB_COMMUNICATION.CSV

<img src="data\img\2024-04-08 155314.png">

## DB_NARROWING_DOWN.CSV

<img src="data\img\2024-04-08 155350.png">

## DB_SORTING_ORDER.CSV

<img src="data\img\2024-04-08 155400.png">

## TARGET_DEVICE.CSV

<img src="data\img\2024-04-08 155623.png">

## DEVICE_TAG.CSV

<img src="data\img\2024-04-08 155700.png">

## DEVICE_TAG_COMPONENT.CSV

<img src="data\img\2024-04-08 155824.png">

## TARGET_SERVER.CSV

<img src="data\img\2024-04-08 155901.png">

## ACCESS_TABLE.CSV

<img src="data\img\2024-04-08 155945.png">

## ACCESS_FIELD.CSV

<img src="data\img\2024-04-08 160037.png">

## NETWORK.CSV

<img src="data\img\2024-04-08 154848.png">

## LOCAL_VARIABLE.CSV

<img src="data\img\2024-04-08 154219.png">

## GLOBAL_VARIABLE.CSV

<img src="data\img\2024-04-08 154228.png">

## DB_BUFFER.CSV

<img src="data\img\2024-04-08 154753.png">

## SECURITY.CSV

<img src="data\img\2024-04-08 154212.png">

## DOT_MATRIX_LED.CSV

<img src="data\img\2024-04-08 154236.png">

## USER.CSV

<img src="data\img\2024-04-08 154202.png">