とりあえずデザインをいじってみたい人のためのメモ。
-------------------------------------------------

試行錯誤しながら書いてるので読みにくいです。

# 手順

検証環境はLinux Mint 14ですが、たぶん最新のUbuntuでも動くんじゃないかな。

## タイルの生成まで

まず、このリポジトリを手元に持ってくる。べつにこのリポジトリじゃなくても、元ネタの openstreetmap/mapnik-stylesheets でもいいですよ。

    mkdir ${HOME}/sandbox
    cd ${HOME}/sandbox
    git clone https://github.com/openstreetmap/mapnik-stylesheets.git

海岸線のshapeファイルを拾ってくる。それなりに大きくて時間かかるかも。1GBくらいは覚悟すること。

    cd mapnik-stylesheet
    ./get-coastlines.sh

元になるOpenStreetMapのデータを持ってきます。Planet.osmから全件取っても(27GB)、GeoFabrik.deから日本のデータを持ってきてもいいですが(800MB)、データが大きすぎるので、BBbike.orgからTokyoのデータを持ってきます。以下。だいたい20MB程度。

    wget http://download.bbbike.org/osm/bbbike/Tokyo/Tokyo.osm.gz

ではもろもろをインストール。まずはPostGISから。

    sudo apt-get install postgresql-9.1-postgis osm2pgsql

インストールしたら、PostgreSQLは勝手に起動してました。

osm2pgsqlは標準リポジトリのは0.80.0で、64bitのkey spaceに対応してません。PPAからインストール。 http://wiki.openstreetmap.org/wiki/Osm2pgsql にしたがって次の手順でインストール。

    sudo add-apt-repository ppa:kakrueger/openstreetmap
    sudo apt-get update
    sudo apt-get install osm2pgsql

mapnikも標準のリポジトリだと2.0.0でちょっとバージョンが低いので、PPAからインストール。せっかくなのでいま最新の2.1.0を入れちゃいます。 https://github.com/mapnik/mapnik/wiki/UbuntuInstallation を参考に。

    sudo add-apt-repository ppa:mapnik/v2.1.0
    sudo apt-get update
    sudo apt-get install libmapnik mapnik-utils python-mapnik

DB作る。usernameは自分にしておくとめんどくさくないです。ちゃんとしたサーバを作りたいならその限りではないけど。...DBはosm2pgsqlインストール時に自動的に作られるかも。

    sudo su - postgres
    createuser (username) --no-createdb --no-createrole --no-superuser --no-password
    createdb --owner=(username) gis
    psql -d gis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    psql -d gis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
    psql -d gis -f /usr/share/postgresql/9.1/contrib/postgis_comments.sql
    psql -d gis -c 'ALTER TABLE geometry_columns OWNER TO (username);'
    psql -d gis -c 'ALTER TABLE spatial_ref_sys OWNER TO (username);'
    psql -d gis -c 'ALTER VIEW geography_columns OWNER TO (username);'
    exit

データを入れてみよう。DB名はデフォルトだし、DBのオーナーを自分にしてるし、ident認証されるからパスワードも不要。変更した人は適当に読み替えて...

    osm2pgsql Tokyo.osm.gz

では設定ファイル作る。上記同様パスワードとか入れないでも大丈夫です。

    ./generate_xml.py --dbname gis --user (username) --accept-none

なんと！これで設定完了です。設定ファイルと座標を与えれば、タイルのpngを作ってくれるプログラムがありました。早速使ってみます。座標は実際のosmあたりから適当に選んで...

    livetiles/render_single_tile.py osm.xml 17 116399 51623 > tile.png

日本語のフォントがトーフになってますが、出力されました。もう少し調整すれば環境を作れそう。

## フォントの設定

じゃ、フォント直しますか。ちょっとググったところ、mapnikのフォントの検索先はこんな感じでわかるみたいです。

    python -c "import mapnik2;print mapnik2.fontscollectionpath"

いまのところ、 /usr/share/fonts/truetype/ttf-dejavu の下を見てるみたいですね。じゃあここに日本語のフォントのシンボリックリンク作っちゃいます。
Linux Mint(っていうかubuntu,debian全般？)だと、 /etc/alternatives/fonts-japanese-gothic.ttf ってのがあるようですねぇ。

    sudo ln -s /etc/alternatives/fonts-japanese-gothic.ttf /usr/share/fonts/truetype/ttf-dejavu/

調べてみたところ、Takao PGothicなるフォントの模様。更に試行錯誤したところ、 inc/fontset-settings.xml.inc の各FontSetに次の設定をすれば日本語が出力されました。

    <Font face-name="TakaoPGothic Regular" />

じゃあ、これでデザインはいじり放題ですね。いじる対象はosm.xml(タイル作成時にファイル名を指定できるのでコピーしてもOK)と、そこから参照されるinc以下の各ファイルですよ。

## 簡易サーバ

render_single_tile.pyに引数を設定してタイルを生成するのが面倒なので他のソースを眺めてみたところ、wsgiをちょっと改変すればサーバを立てられることがわかったので、作ってみました。
livetiles/livetiles.conf を記述して、

    cd livetiles
    ./simple_tileserver.py

ってすれば、 http://localhost:8080/stylename でOpenLayersを使った地図が表示できます。
mod_tileとちがってキャッシュしないので遅いですが、毎回描画してくれるのでデザインいじりながら使うにはいいかも。


# ボツ案

データ取得部分は、当初は以下の文書にしてました。でもレンダリングしたところデータが変な部分があったので却下。そのうち検証してみます。→レンダリングがおかしかったのは、古いosm2pgsqlを使ったせいで64bit idが正しくDBに入ってなかったからだったらしい。

# データの取得 ボツ案

元になるOpenStreetMapのデータを持ってきます。Planet.osmから全件取っても(27GB)、GeoFabrik.deから日本のデータを持ってきてもいいですが(800MB)、データが大きすぎるのでここはひとまず密度の濃そうな新宿、渋谷あたりのデータをOverpass APIを使って取得してみます。bounding boxの順番は南西北東らしいです。

    wget -O map.osm "http://overpass-api.de/api/interpreter?data=(node(35.6433,139.6852,35.6985,139.7167);<;);out;"

wgetコマンドの結果によると、19,877,133  57.8K/s   時間 6m 41s とのことでした(無圧縮で)。このサイズだったらBBbike.orgからTokyoのデータを持ってきたほうがいいかもですね。20MB程度に圧縮されたデータが入手できます。
