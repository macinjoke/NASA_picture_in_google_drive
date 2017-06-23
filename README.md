# NASA_picture_in_google_drive

![Astronomy Picture of the Day](https://raw.githubusercontent.com/wiki/tonkatu05/NASA_picture_in_google_drive/images/ISSLightShow_nasa_4928.jpg)

> https://apod.nasa.gov/apod/astropix.html より

# 概要
Macの壁紙を自動で変わる高画質宇宙画像にする。 Windowsでもおそらく可能。
- サーバー側で自動でAstronomy Picture of the Day (NASA)から画像を取ってきてGoogle Drive に入れる
- Macの壁紙の設定でGoogle Driveのフォルダを指定し、壁紙が自動で変わるようにする

# 詳細
Googole Drive の APIで以下の操作をする。

- 半永久的に宇宙画像を貯めるフォルダを１つ作る
- そのフォルダの中の宇宙画像ファイルを作成日時が新しい順に5つ壁紙用フォルダにコピーする(既に壁紙用フォルダに画像が存在するなら、5つになるように調整する)

Mac側の設定でn分間隔で壁紙をフォルダ内の画像で切り替える設定が可能。ユーザーは壁紙用フォルダを指定しておくと、1日あたり5つの宇宙画像が見れ、かつ毎日1つずつ更新される。

# 補足
(2017/6/23更新)
どこかにデプロイしようと思っているけどやっていなくて放置している状態。今度やる。サービス化したい。
サービス化にあたってはWeb上でGoogle Driveの認証へ飛ばしたり、壁紙画像変更の細かい設定ができると良いな。
