３ノードからなる、推移予測システムプロトタイプ

ダイクストラの最小コストによる最短距離を探索するロジックを利用して
買い物履歴のルート探索をおこなう

カートインのシーケンスについて・・
1番目に選んだ品物は2番目に選ぶ商品に影響を与えると考えられる。
たとえばアパレルなど1番目にシャツを選び、これに合うパンツなどを合わせ買いをすることが考えられる

さらに1番目→2番目というシーケンスに続く商品についても
嗜好性＆指向性があると仮説を立てて、実際にどんな結果が導かれているか検証しようと考えた

当初、SparkのGraphライブラリを使ったシステムにトライしていたが考えていたほどスピードが出ないことがわかり
また、ありもののライブラリを使うときめ細かいチューニング、ボトルネック調整などができないことも分かったので
とりあえず簡単に検証できるpythonをつかっている

市井に転がっているダイクストラのサンプルでは任意の始点で始まり且つ、終点が定まらないようなロジック
では、まともに動作しなかったので、アルゴリズムを咀嚼しながらすべて自前で実装してみた
（このため、一般的なダイクストラとは違った動き、あるいは車輪の発明になっているかもしれないのであしからず）

テストデータから実データに切り替えて施行する段階で全探索すると計算に非常に時間がかかることがわかり
無向グラフを有効グラフに切り替えたり、探索深度を設定して処理を切り上げたりしている
テストでは探索深度を１０程度にしている（２０だと終わらない・・分割して並行処理すればいけるのかもしれない）

現状、python上の連想配列を使ってGraph構造をつくっているが、この部分を外部のキーバリュー（redisなど）に
切り替えてみたい、また購買履歴の動きが陳腐化することも考えられるので、Graph構造上のデータを
一定の間隔で世代交代させる仕組みも考えたい

現状

探索モデルのフロー20200519

●サンプルをログから抜き出してくる・・
TODO　手作業でやっているので、あとで作りこむ・・

●サンプルデータからカートイン情報を抜き出し加工する
python LogTraceV05.py

●ルートを探索する

python dijkstraV03.py "502684808-000"

●ルート上のアイテム情報をDBより取得する

python getMaster.py

●ルート情報とマスター情報を合成して出力イメージを作る

python route2html.py


Docker関連メモ

docker上のシェルに入る
sudo docker-compose exec python3 bash

インストールしたものメモ
root@dd0c40644490:~# history | grep install
   45  apt-get install -y apt-utils apt-transport-https
   48  apt-get install -y msodbcsql17
   50  apt-get install -y msodbcsql17
   51  apt-get install -y mssql-tools
   52  apt-get install -y unixodbc-dev
   53  pip install --upgrade pip
   54  pip install pyodbc
   66  apt-get install -y apt-utils apt-transport-https
   70  apt-get install -y msodbcsql17
   71  apt-get install -y mssql-tools
   72  apt-get install -y unixodbc-dev
   73  pip install --upgrade pip
   74  pip install pyodbc
   85  wget https://gallery.technet.microsoft.com/ODBC-Driver-13-for-Ubuntu-b87369f0/file/154097/2/installodbc.sh
   86  sh installodbc.sh
  105  history | grep install

