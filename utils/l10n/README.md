localization memo

出力する地図を日本語化するメモ
手順は次のとおり。

* osm2pgsqlの設定ファイルdefault.style をコピー
* コピーしたファイル(ここではja.styleとしとく)に項目name:jaを追加
* osm2pgsqlを使用してデータベース作成。このとき、オプションを指定して上記ファイルを使用する(例: osm2pgsql -hlocalhost -Uosm -dgis -sja.style japan.osm.pbf)
* データベースにビューを作成する。本ファイルと同じディレクトリにあるcreate_script.shをいい感じに直して実行すると、ビューを作るためのsqlを作ります。
* mapnikなどで使用するスタイルシートの設定を変更し、上記で設定したビューを使用するようにする。
