# FOSS4G 2026 Hiroshima 口頭発表 スピーカーノート（英語原稿・日本語原稿・非発話の補足）

英語本文は壇上で読む原稿、日本語本文は練習・自己確認用の原稿です。本書は12枚版の生成用正本です。指定PPTXの最終11枚版（英日9組・英語1,064語）と同期した原稿は、[最終11枚版スピーカーノート](exp002_kitagi_foss4g2026_presentation_delivery_notes_11slides.md) に記載しています。

---

### Slide 1 — Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

Good afternoon. Please take a look at this wall. It is not natural: people quarried granite on this island for about four hundred years, and the water at its base collected after the cutting stopped. This is a photograph I took on the island, not a map or an analysis result. Over the next twenty minutes, I will show you this same island at three different scales.

こんにちは、まずこの壁を見てください。これは自然の崖ではありません。この島では約400年にわたって花崗岩が切り出され、底の水は採石が止まったあとに溜まりました。これは私が島で撮った写真で、地図でも分析結果でもありません。これから20分間、同じ島を三つの違う縮尺でお見せします。

**JA（補足・読み上げない）**

- 冒頭では「この崖は自然のものではない」を固定する。写真は現地写真であり、検出結果ではない。

---

### Slide 2 — A quarrying island, and the ponds it left behind

Kitagi Island is in the Seto Inland Sea, in Kasaoka City, Okayama Prefecture, and it is the largest of the Kasaoka Islands. Granite quarrying began there in the early seventeenth century; at its 1957 peak, 127 sites operated and as many as 12,000 people lived there, compared with two working quarries and roughly 600 to 700 residents today. Many abandoned pits were not backfilled, so rainwater and groundwater turned some of them into ponds in a landscape where people still live and work. The island became part of the national heritage “Stone Islands of Setouchi” in 2019, which increased interest in this quarry landscape. I went looking for an island-wide inventory of these water bodies, but I found only partial records, so that describes my search rather than proving that no records exist.

北木島は瀬戸内海の岡山県笠岡市にあり、笠岡諸島で最大の島です。17世紀初めから花崗岩が切り出され、1957年のピークには127か所が稼働し、1万2千人ほどが暮らしていましたが、現在は稼働中の丁場が2か所、住民は600〜700人ほどです。採石をやめた穴の一部は埋め戻されず、雨水や地下水が溜まって池になり、今も人が暮らし働く景観に残っています。2019年には「石の島」として日本遺産になり、丁場景観への関心が高まりました。そこで島全体の水域目録を探しましたが、見つかったのは部分的な記録であり、記録が存在しないと断定しているわけではありません。

**JA（補足・読み上げない）**

- 「見つからなかった」は探索範囲の限定であり、存在しないという断定ではない。

---

### Slide 3 — On foot: I could stand in front of five or six of them

My story with the island began in March, at a two-day drone-mapping party. On foot, I first noticed the sharply cut walls, and then the deep green water. Published records report depths ranging from a few metres to about twenty metres, but I did not measure those depths myself. One flooded quarry even has a small wooden stage on the water, with stone blocks for seats. During those two days, I visited only five or six quarry sites by foot or by car, and that small number is the reason this talk exists.

私とこの島の話は、今年3月の二日間のドローン・マッピングパーティから始まりました。歩いてまず気づいたのは、風化ではなく切り出された、まっすぐな壁です。次に見えたのが深い緑の水で、公開記録には水深が数メートルから約20メートルとありますが、これは私の計測値ではありません。水没した丁場のひとつには水上の木のステージがあり、石の塊が客席のように並んでいます。その二日間に私が訪れたのは徒歩か車で5〜6か所だけで、この小さな数字が今回の発表の出発点です。

**JA（補足・読み上げない）**

- 水深は記録由来であり著者の計測値ではない。5〜6か所は後半の規模対比の伏線で、訪問地点を検出ポリゴンに照合したものではない。

---

### Slide 4 — From the air: the quarry boundaries are the landform

On the second day, we flew the drone from the stage, and the island changed shape: from the air, the quarries looked like grey rectangles cut into a green canopy. Between two pits, a thin granite wall remains because two companies once kept their quarry boundary intact, turning a line on a legal document into a landform. That boundary was the surprising part of the aerial view. The wall is invisible from inside either pit and too thin to notice in ten-metre satellite imagery, so this is a qualitative observation from the air, not a measurement from this study. We also added features visible on the ground to OpenStreetMap, but that did not create an island-wide inventory.

二日目にステージからドローンを飛ばすと、島の形が変わって見えました。上空では、丁場が緑の樹冠に切り込まれた灰色の四角形として見えます。二つの会社が採石の境界を守ったため、二つの穴の間には細い花崗岩の壁が残り、書類の上の線が地形になっています。その壁は穴の中からは見えず、10メートルの衛星画像でも細すぎるため、これは上空からの定性的な観察であって研究の測定結果ではありません。私たちは地上で見た地物をOpenStreetMapに追加しましたが、島全体の目録にはなりませんでした。

**JA（補足・読み上げない）**

- 境界が地形になったという説明は現地での定性的観察であり、本研究の測定結果ではない。OSMへの追加も観察できた範囲に限る。

---

### Slide 5 — On the train home: one satellite scene covers the whole island

On the train home, I realised that five or six sites were only a small part of the island, while one free satellite instrument could cover it in a single frame. I downloaded a Sentinel-2 Level-2A scene through the Microsoft Planetary Computer STAC API: 2 August 2025, with 0.7 percent reported cloud, on a ten-metre grid. The workflow is standard, not new. NDWI and MNDWI flag likely water, while NDVI masks vegetation. I used thresholds of −0.2 for NDWI, −0.1 for MNDWI, and 0.3 for NDVI. Because a ten-metre pixel can mix water, granite, and shadow, I chose these thresholds from histogram valleys, without optimisation, sensitivity analysis, or field checking. I resampled the 20-metre short-wave infrared band to a ten-metre output grid and retained polygons of at least 100 square metres.

帰りの電車で、5〜6か所は島のほんの一部ですが、無料の衛星なら一枚で島全体を覆えると考えました。Microsoft Planetary ComputerのSTAC APIから、2025年8月2日、報告雲量0.7％、10メートル格子のSentinel-2 Level-2Aシーンを取得しました。手順自体は標準的で、新しい手法ではありません。NDWIとMNDWIで水域候補を抽出し、NDVIで植生を除きました。閾値はNDWIが−0.2、MNDWIが−0.1、NDVIが0.3です。10メートル画素には水・花崗岩・影が混ざるため、閾値はヒストグラムの谷から選び、最適化・感度分析・現地確認はしていません。短波赤外の20メートルバンドを10メートルの出力格子にリサンプリングし、100平方メートル以上のポリゴンだけを残しました。

**JA（補足・読み上げない）**

- STACは「S-T-A-C」と読む。標準手法であり新規性を主張しない。閾値の由来と未検証の留保は削らない。

---

### Slide 6 — The scan found 145 water polygons across the island

From one summer scene, the scan found 145 water polygons inside the island, each at least 100 square metres. The spring scene from 23 March 2025 had 0.0 percent reported cloud and 113 reported polygons, with a largest area of 1.28 hectares. The summer scene from 2 August had 0.7 percent reported cloud and 145 polygons, with a largest area of 7,826 square metres. The scenes differ, but we have not isolated the cause. The spring run reported 113 polygons, but its exact processing configuration was not preserved, so I treat 113 as a reported value with a reproducibility limitation, not as evidence of a seasonal difference. The NDVI mask removed only nine pixels, and the polygons cluster in the north, south-east, centre, and west, where historical quarry records also cluster. These are detected water polygons, not individually field-confirmed quarry ponds, so I report no precision or recall; the imagery is modified Copernicus Sentinel data from 2025.

夏の一つのシーンから、島内に100平方メートル以上の水域ポリゴンが145件出ました。2025年3月23日の春シーンは報告雲量0.0％、報告値113件、最大1.28ヘクタールでした。8月2日の夏シーンは報告雲量0.7％、145件、最大7,826平方メートルでした。二つのシーンには差がありますが、原因は特定できておらず、春の実行設定も保存されていません。そのため113件は季節差の証拠ではなく、再現性に限界のある報告値として扱います。NDVIマスクが外したのは9画素だけで、ポリゴンは歴史記録と同じく北・南東・中央・西に集中しました。これらは一件ずつ現地確認された丁場池ではない検出された水域ポリゴンであり、適合率や再現率は報告しておらず、画像は2025年の加工済みCopernicus Sentinelデータです。

**JA（補足・読み上げない）**

- 145件は水域ポリゴン候補であり、丁場数ではない。113件は当時の報告値で、現行設定での再現値ではない。S6は2分30秒以内を目安にする。

---

### Slide 7 — Each scale shows what the others cannot

Putting the three scales together shows the main lesson from the island. On foot, I got texture: cut faces, green water, and a sense of depth, but only one place at a time. From the air, I got boundaries, including the granite wall left between two companies. From orbit, I got the island-wide distribution: 145 candidates from one frame. None of these scales is better than the others; they reveal different parts of the problem, and relying on only one can leave the rest unseen.

三つの縮尺を並べると、この島から得られる教訓が見えてきます。歩いて得られたのは、切られた面や緑の水、深さの感じといった質感ですが、一度に見られるのは一か所です。つまり地上では、島全体の分布までは見渡せません。上空からは、二つの会社の間に残る花崗岩の壁を含めた境界が見え、軌道上からは一枚の画像で島全体の145件の候補という分布が見えました。三つに優劣はなく、それぞれ見えるものが違うので、ひとつの縮尺だけに頼ると問題の一部を見落とします。

**JA（補足・読み上げない）**

- 145は候補または検出であり、丁場数と読める言い方はしない。

---

### Slide 8 — Five or six sites visited — the scan produced 145 candidates

Here are the two numbers that frame the talk: I stood in front of five or six sites, while one satellite scene produced 145 water-polygon candidates. That gap is the practical value of scanning the whole island first. I am not saying those five or six correspond to five or six of the 145, because I never matched my visits to individual polygons, and none is field-confirmed. Some OpenStreetMap quarry features overlapped the detected polygons, but OSM is not ground truth, so overlap proves neither identity nor accuracy. The scan does not tell us how many drowned quarries exist; it provides a finite list to prioritise for fieldwork, subject to access, safety, and permission.

この発表を枠づける数字は二つです。私が立ったのは5〜6か所で、衛星の一つのシーンからは145件の水域ポリゴン候補が出ました。私の5〜6か所が145件のうちの5〜6件だとは言えません。訪問場所を個別ポリゴンに対応づけておらず、どの候補も現地確認済みではないからです。比較ではOpenStreetMapの丁場地物が検出と重なりましたが、OSMは正解データではないため、重なりは同一性も精度も証明しません。走査は水没した丁場の数を教えるのではなく、安全・立入許可・到達可能性を踏まえて現地調査の優先順位を付ける有限のリストを与えます。

**JA（補足・読み上げない）**

- OSMは参考値であり、精度・一致とは呼ばない。訪問地点が検出集合の部分集合だとは主張しない。

---

### Slide 9 — Two days ago I went back — a first look, not validation

This slide shows my return visit on 31 August: it is a first look, not validation. I selected candidates using their coordinates and areas, but safety, permission, and walkability mattered more than area ranking, so these were candidates selected for possible visits, not an accuracy sample. The visit therefore tests the workflow, not its accuracy. The photographs show what the scan pointed at from the ground; they do not identify historical quarries or provide a count of correct and incorrect detections. The important change is that the list comes first: instead of wandering and finding ponds by chance, I can use open data and open-source code to decide where to look next.

このスライドは8月31日の再訪を示しますが、これは最初の確認であって検証ではありません。候補の座標と面積から短いリストを作りましたが、面積順位よりも安全、許可、歩いて行けるかどうかを優先したため、精度評価用の標本ではなく訪問を試みる候補です。写真は走査が指した場所を地上から見たもので、歴史記録上の丁場の同定や、正誤の集計を示すものではありません。大きな変化はリストが先に来たことです。歩き回って偶然池を見つけるのではなく、オープンデータとオープンソースのコードで次に見る場所を決められます。

**JA（補足・読み上げない）**

- **[UPDATE AFTER 2026-08-31]** 再訪後に写真と実際の状況に合わせて見直す。写真は候補の存在を示すだけで、accuracy validationではない。

---

### Slide 10 — What this can and cannot tell you

Before going further, I want to be explicit about the limits. At ten metres, narrow ponds are unreliable, and thresholds below zero can also classify dark rock and shadow as water. I also have no precision or recall because field validation has not been done. The scan detects water, not quarries, so natural ponds, irrigation reservoirs, tanks, and even shoreline sea can enter the result, while the vegetation mask changed only nine pixels in this run. The next steps are to walk the candidates, add a land mask, and try higher-resolution imagery for narrow ponds; none requires a new method, but all require someone to look.

ここから先へ進む前に、この結果の限界を明示します。10メートル解像度では細い池が不確かで、ゼロ未満の閾値は暗い岩や影も取り込むため、現地検証をしていない私は適合率も再現率も出せません。検出しているのは丁場ではなく水域なので、自然の池、ため池、貯水施設、海岸線の海も入り得ますし、今回の植生マスクが変えたのは9画素だけでした。次は候補を歩き、陸域マスクを加え、細い池には高解像度画像を試します。新しい手法よりも、誰かが現地へ行って見ることが必要です。

**JA（補足・読み上げない）**

- 限界は短く言い切る。次の課題は新手法ではなく現地確認である。

---

### Slide 11 — The 145 polygons are open data now

To make that fieldwork possible, the 145 polygons are now public as GeoJSON in EPSG 4326, ready to open in QGIS. The public release is the detected polygons. Raster outputs written by the pipeline for fieldwork and heritage documentation are output formats, not published datasets. The workflow uses open-source Python libraries such as Rasterio, NumPy, and Shapely, with no licence fees or imagery to buy. It could extend to other quarried islands, but do not reuse my thresholds unchanged: they came from this island, this season, and this water. The work is released under CC BY 4.0, using modified 2025 Copernicus Sentinel data.

現地調査を可能にするため、145件のポリゴンをEPSG 4326のGeoJSONとして公開しています。公開しているのは検出ポリゴンです。パイプラインが現地調査や遺産記録向けに書き出すラスタは、出力形式であって公開データセットではありません。手順はRasterio、NumPy、ShapelyなどのオープンソースPythonライブラリで動き、ライセンス費用も画像購入も必要ありません。他の採石の島にも広げられますが、閾値をそのまま持ち込んではいけません。この島、この季節、この水のヒストグラムから導いた値だからです。成果は、2025年の加工済みCopernicus Sentinelデータを用いたものとして、CC BY 4.0で公開しています。

**JA（補足・読み上げない）**

- EPSGは「E-P-S-G four three two six」と読む。GeoJSONとラスタ出力を混同しない。

---

### Slide 12 — Check them on the ground, then put them on the map

The loop I want to leave you with is simple: a satellite scan turns an unknown into a finite candidate list, and a field visit turns a candidate into something seen with your own eyes. OpenStreetMap then turns what you confirm into a public map that anyone can use, instead of leaving it in a private working file. I plan to contribute only the ponds I can actually confirm, but that is still a plan and I have not done it yet. In March, we mapped what we saw on the ground; now the scan suggests where to look next, and that is the whole idea. Thank you, and I am happy to take questions.

最後に残したい循環はシンプルです。衛星の走査が未知のものを有限の候補リストに変え、現地訪問が候補を自分の目で見たものに変えます。OpenStreetMapは、確認したものを私だけのファイルから誰でも使える公共の地図へ変えます。私は実際に確認できた池だけを提供する計画ですが、まだ実行していません。3月には地上で見たものを地図に追加し、今度は走査が次に見る場所を示し、それがこの考え方の全体です。ありがとうございました。質問をお受けします。

**JA（補足・読み上げない）**

- OSMへの還元はまだ計画であり、既に実施したとは言わない。前向きな循環で締める。
