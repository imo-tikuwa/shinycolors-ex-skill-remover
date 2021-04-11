# shinycolors-ex-skill-remover

## このリポジトリについて
[enza版 アイドルマスターシャイニーカラーズ](https://shinycolors.enza.fun/)（以下シャニマス）のExスキルを自動で外すツールです。

## 開発環境
 - OS : Windows 10 PRO
 - IDE : VSCode
 - Monitor : 24インチ フルHD(1920x1080) × 2
 - python : 3.8.2
 - pip(venv) : 19.2.3
 - GoogleChrome : 89.0.4389.114
 - chromedriver : 88.0.4324.96

※exec_chrome.bat、settings.iniの中で自分の環境用に決め打ちしてる変数、パスがあります

## 環境構築
```
python -m venv venv
venv/Scripts/activate.bat
pip install -r requirement.txt
```

## プログラムについて
### exec_chrome.bat
GoogleChromeをremote-debugging-portオプション付きで起動するバッチファイル

### app.py
メインのプログラム。

### commons.py
app.pyやcrop_〇〇_image.py用の共通処理をまとめたプログラム。

### generate_npz_data.py
テンプレートマッチングに使用する画像を1つのファイルにまとめるプログラム。

### crop_〇〇_image.py
起動中のシャニマスの指定領域をサンプルデータとして切り出すプログラム。

## 免責事項
 - 当リポジトリのプログラムを利用した事によるいかなる損害も作者は一切の責任を負いません。
 - 株式会社バンダイナムコエンターテインメント様、株式会社BXD様とは一切関係ございませんので、そちらへの問い合わせ等はお控えください。
