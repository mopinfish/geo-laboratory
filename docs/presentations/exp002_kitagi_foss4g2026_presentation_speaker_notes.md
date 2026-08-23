# FOSS4G 2026 Hiroshima 口頭発表 スピーカーノート（英日併記）

発話対象は英語（`EN (spoken)`）のみ。日本語（`JA (not spoken)`）は訳と留意点であり、
壇上では読み上げない。英語は箇条書きではなく、読み上げる文章そのものを書いている。

各スライドの英語は、発表時間の割り当て（合計1,050秒）を 145 wpm で換算した語数を目安に
している。通し読みで押している場合は、数値と留保（候補である旨・精度指標の不在・
春季値の由来）を残したまま、情景描写の側から削る。

同じ内容が PPTX のノートペインにも入っている（英語→日本語の順）。

---

### Slide 1 — Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

**EN (spoken)**

Good afternoon. Before anything else, please look at the wall in this picture. This cliff is not natural. People cut it, block by block, for about four hundred years. The water at the bottom arrived later, after the cutting stopped. This is a photograph I took on the island myself. It is not a map, and it is not a result from my analysis. My name is Noboru Otsuka, and I work at Geolonia. For the next twenty minutes I will show you the same island at three different scales.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 「この崖は自然のものではない」から入る。人が約400年かけて切り出した面で、水はその後に溜まったもの。写真は著者が現地で撮影したもので、検出結果の図ではない。
- 冒頭の一言は「この崖は自然のものではない」に固定する。ここで手法の話をしない。
- 表紙写真は現地写真。検出結果の可視化と誤解されないよう「結果ではない」と明言する。

---

### Slide 2 — A quarrying island, and the ponds it left behind

**EN (spoken)**

So, where are we? Kitagi Island sits in the Seto Inland Sea, in Kasaoka City, Okayama Prefecture. It is a small island.

People have been cutting granite there since the early seventeenth century. At the peak, in 1957, the island had one hundred and twenty-seven active quarry sites, and up to twelve thousand people lived there. Today there are two working quarries, and about six to seven hundred residents.

Here is the part that matters for this talk. When a quarry stops, nobody fills the pit back in. Rain and groundwater arrive instead, and the pit becomes a pond. So the island is left with a large number of flooded holes, in a landscape where people still live, still work, and still walk around.

In 2019 the island became national heritage, as one of the "Stone Islands of Setouchi". Heritage means visitors come to look at exactly these places.

And that is where my problem started. I went looking for a list of the ponds. Where are they? How big are they? How many are there? I found no island-wide record of the ponds themselves.

I want to be careful with that sentence. It describes my search, not the world. Partial records do exist, and I will come back to them later in the talk. What I could not find was an inventory of the water bodies for the island as a whole.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 位置（瀬戸内海・岡山県笠岡市）、17世紀初頭からの採石、1957年ピークで127丁場・人口1万2千人、現在は稼働2丁場・住民600〜700人。廃止後の丁場に雨水と地下水が溜まって池になる。2019年に日本遺産「石の島」認定。島全体の池の記録は見つからなかった。
- 「見つからなかった」は**探索範囲の限定**であって、存在しないという断定ではない。この留保を英語で必ず言う。
- オープンデータに部分的な記録があることはS8で参考として触れる。ここでは「後で戻る」とだけ言う。
- 石材の用途（城壁・橋・著名建築）は権威資料に含まれていないため語らない。

---

### Slide 3 — On foot: I could stand in front of five or six of them

**EN (spoken)**

My own story with the island starts in March this year, at a drone mapping party. A group of people who like maps came over for two days, to fly drones and to add what we saw to the map.

Walking around, the first thing you notice is the walls. They are vertical, and they are flat, and they are clearly cut rather than weathered. You can still read the lines where the stone was split.

The second thing you notice is the water. It is green. Not the green of a dirty pond — a strange, mineral, glowing green. The published descriptions give depths from a few metres to about twenty metres. That figure comes from the record, not from anything I measured. Standing at the edge, you believe it.

And then there is the stage. One of the flooded quarries has a stage built out on the water, made from the stone that was left behind. In front of it, blocks of stone are laid out as seats. The island sometimes uses the place as a venue for events.

Now, the important number on this slide is a small one. Five or six sites during the event. That is how many quarry ponds I stood in front of, in two days, on foot. It felt like a lot at the time. Please remember that number, because it comes back later, and it is really the reason this talk exists.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 2026年3月のドローン・マッピングパーティ参加が出発点。垂直で平らな切削面、緑がかった水面、数メートル〜約20メートルとされる水深、余った石材で作られた湖上ステージと、座席代わりに並べられた石（湖上イベントの会場として使われることがある）。イベント中に立ったのは5〜6か所。
- 水深は報告書由来の記述であり著者の計測値ではない。英語でも "from the record, not from anything I measured" と必ず言う。
- 徒歩スケールで分かるのは**質感**だけ。島全体は見えないという流れをS7へつなぐ。
- 「5〜6か所」はS8の規模対比の伏線。ここで数字を印象づける。

---

### Slide 4 — From the air: the quarry boundaries are the landform

**EN (spoken)**

On the second day we flew from the stage on the water. And the island changed shape.

From a hundred metres up, the quarries read as grey rectangles cut into a green canopy. Straight edges, right angles, sharp corners. Nothing else on that island looks like that.

The thing I did not expect is what sits between them. Where two companies held quarrying rights next to each other, neither side cut the boundary. So a thin wall of granite is left standing between the two pits. A property line, standing as terrain. A line on a legal document became a landform.

You cannot see that from the ground, because you are inside one pit or the other. And from orbit, at ten metres, the wall is too thin to notice. You can only see it from a few hundred metres up.

I should be clear that this is me looking and describing. It is a qualitative observation from that day, not a measurement from this study. We also flew a survey over one of the lakes while we were there.

And one more thing from those two days, which I will pick up again at the end. The same event added features to OpenStreetMap. We put on the map the things we could see on the ground. Which means the map got better in exactly the places where we happened to walk, and nowhere else.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 2日目に湖上ステージからドローンを飛ばした。上空からは緑の樹冠に切り込まれた灰色の矩形として見える。隣接する採石権者の境界は切削されず、細い花崗岩の壁として残る。所有権の線が地形になっている。イベントではOpenStreetMapへの地物追加と湖の測量も行った。
- 境界が地形になっているという観察は**現地での定性的観察**であり、本研究の測定結果ではない。英語でも明言する。
- イベントで追加したのは現地で観察できた地物のみ。徒歩到達範囲を網羅的に地図化したとは述べない。
- 最後の一文（歩いた場所しか良くならない）はS12の「地図に還す」への伏線。

---

### Slide 5 — On the train home: one satellite scene covers the whole island

**EN (spoken)**

On the train home I was still thinking about the five or six ponds I had seen, and about all the ones I had not. There is one instrument that covers the whole island in a single frame, and it is free to use.

I used Sentinel-2, level 2A, pulled through the Microsoft Planetary Computer STAC API. One summer scene, the second of August 2025, with zero point seven percent cloud, on a ten metre grid.

I want to say clearly that this is a standard water-index workflow, and that nothing in the method is new. I used three indices, and they are all simple band arithmetic. NDWI is built from the green band and the near-infrared band. MNDWI is built from the green band and the short-wave infrared band. NDVI, the vegetation index, is built from the near-infrared band and the red band. A pixel counts as water if NDWI is above minus zero point two, or MNDWI is above minus zero point one, and NDVI is not above zero point three.

You may be wondering why two of those thresholds sit below zero. The reason is the pixel size. At ten metres, a narrow pond is part water, part granite and part shadow, all inside one pixel, so a strict positive threshold throws the small ponds away.

I picked the numbers from the valley in the histogram. I did not optimise them, I did not run a sensitivity analysis, and I did not check them in the field. The short-wave band arrives at twenty metres, so I resampled it to ten. And I only report polygons of one hundred square metres or more.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: Sentinel-2 L2A を Microsoft Planetary Computer の STAC API 経由で取得。2025年8月2日・雲量0.7%・10 m グリッド。NDWI＝緑と近赤外、MNDWI＝緑と短波赤外、NDVI＝近赤外と赤。水域条件は（NDWI > −0.2 または MNDWI > −0.1）かつ NDVI > 0.3 でない。負の閾値は10 mでの混合画素への対処。閾値はヒストグラムの谷から決めた値で、最適化・感度分析・現地検証はしていない。短波赤外は20 mから10 mへリサンプリング。報告下限は100 m²。
- 3指数の**式の構成は投影しない**（担当者ルーリング）。したがって「何と何から作るか」は英語の発話で必ず言う。
- 「標準的な手順であり手法の新規性はない」も英語で必ず言う。本発表は手法の新規性を主張しない。
- 閾値の由来（ヒストグラムの谷・最適化なし）はこのスライドの留保。急いでいても削らない。

---

### Slide 6 — The scan found 145 water polygons across the island

**EN (spoken)**

So: one scene, one island, and this is what came out. The scan found one hundred and forty-five water polygons inside the island, each of them at least one hundred square metres.

Let me give you both of the scenes I ran. Spring: 2025-03-23, 0.0% cloud — 113 reported polygons, largest 1.28 hectares. Summer: 2025-08-02, 0.7% cloud — 145 polygons, largest 7,826 square metres.

Now the honest part. The two reported scenes differed, but we have not isolated the cause. It is tempting to say this is the season, and I am not going to say that. The spring figure is what we reported; that run's configuration is not preserved. So please read the spring number as a note from my logbook, and not as a measurement you can stand on.

One result did surprise me. I put the vegetation index into the rule because I expected green water and green canopy to get confused with each other. The NDVI vegetation mask removed only nine pixels. Nine. My worry was simply wrong, and I would rather tell you that than quietly leave it out.

Now look at where the polygons are. They cluster in the north, the south-east, the centre and the west, and that pattern sits on top of where the historical records say the quarrying was. At the peak in 1957 the island had one hundred and twenty-seven recorded quarry sites. My scan returned one hundred and forty-five detections. Those two numbers are close, and I want to be careful here. This is a comparison of scale, and not a one-to-one match. I have not matched detection number one to quarry number one, and I am not claiming that I can.

The line at the bottom of the slide is the one I would most like you to take away. These are detected water polygons, not individually field-confirmed quarry ponds. I have no precision figure and no recall figure, because I have not done the field validation that would produce them. The imagery is modified Copernicus Sentinel data from 2025.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 夏季シーンから島内145件（各100 m²以上）を検出。春季 2025-03-23・雲量0.0%・報告113件・最大1.28 ha、夏季 2025-08-02・雲量0.7%・145件・最大7,826 m²。両者は差があるが原因は特定できていない。春季値は当時の報告値で実行設定が保存されていない。NDVIマスクの除外は9ピクセルのみ（仮説の棄却）。分布は北・南東・中央・西の4集中帯で歴史記録と整合。145対127は規模の比較であって1対1対応ではない。検出は候補であり個別に現地確認されていない。精度指標は算出していない。
- 必須発話6行はこのスライドの契約事項。時間が押しても削らない。
- 季節を原因として断定しない。「原因は特定できていない」で止める。
- 145件は検出数であって丁場数ではない。127との近さを一致として語らない。
- S6単体で2:30以内に収める。押している場合は情景描写ではなく分布の説明を短くする。

---

### Slide 7 — Each scale shows what the others cannot

**EN (spoken)**

Let me stop for a moment and put the three scales next to each other, because I think this is the real lesson from the island.

On foot I got texture. The cut face, the green water, the sense of depth. I could touch the rock. But I could only stand in one place at a time.

From the air I got boundaries. I could see that the line between two companies is a wall of rock, left standing. That is invisible from the ground, and it is too thin to matter from orbit.

From orbit I got distribution. One hundred and forty-five candidates, across the whole island, from a single frame. But at ten metres I cannot tell you whether a wall was cut or weathered.

None of these three is better than the others. Not better or worse — different things become visible. And if you only ever work at one scale, you will be very confident about the wrong shape of the problem.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 徒歩＝質感、上空＝境界、衛星＝分布。三つは優劣ではなく別のものを見せる。ひとつの縮尺だけで作業すると、問題の形を取り違えたまま確信を持ってしまう。
- 本スライドは解釈の提示であり、新しい数値は出さない。
- 「145 candidates」と言う（detections でも可だが、丁場数と読める言い方はしない）。

---

### Slide 8 — Five or six sites visited — the scan produced 145 candidates

**EN (spoken)**

Let me put the two scales side by side, because this gap is the whole point of the talk. During the mapping party I stood in front of five or six quarry sites. From a single satellite scene I got one hundred and forty-five water polygons.

I am not saying that my five or six are five or six of the 145. I never matched the places I visited to individual polygons, so please hear this as a contrast of scale and nothing more. Individual ponds are not field-confirmed. There is no precision and no recall yet.

I can offer you one reference point. Every quarry feature that is already mapped in OpenStreetMap overlaps one of my detections. I pulled that comparison in late August, and I am showing it as a reference, not as ground truth. OpenStreetMap is not an accuracy benchmark, and an overlap does not mean the two records describe the same feature. So I will not call it agreement, and I will not turn it into a percentage.

What I do have is something I find more useful than a percentage. Before the scan, the honest answer to "how many drowned quarries are on this island" was: nobody knows. After the scan, the answer is: here are 145 places to go and look. The candidates form a finite field-check list. And a finite list is something a small group of people can actually work through.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 訪問5〜6か所に対し、1シーンから145件の検出。訪問地点を個別ポリゴンに照合した記録はないため、これは規模の対比にとどまる。個別の池は現地確認されておらず、精度指標もない。OSMに既に登録済みの丁場地物はいずれも検出と重なるが、これは参考値であって正解データではない。重なりは同一地物の同定を意味しない。候補は有限の現地確認リストになる。
- OSMは参考値。件数の内訳・距離の定義・感度は投影せず、口頭でも数値化しない（質疑で聞かれた場合のみ想定問答で答える）。
- 訪問地点が検出集合の部分集合であるとは主張しない。この否定を英語で必ず言う。
- 到達可能性は安全・立入許可に依存する。「歩けば全部確認できる」とは言わない。

---

### Slide 9 — Two days ago I went back — a first look, not validation

**EN (spoken)**

Now, two days ago, on the thirty-first of August, I went back to the island. I want to be very clear about what this is and what it is not. This is a first look. It is not validation.

Here is how I chose where to go. I opened the published set of one hundred and forty-five polygons, and I made a short list of candidates with their coordinates and their areas. Then I threw most of that ranking away, because on a working quarry island, safety, permission, and simply being able to walk to a place matter more than which pond is the biggest. So these are not a sample designed for accuracy. They are the candidates I could reach.

What you are looking at are illustrative field photographs from that day. They show what the scan pointed at, seen from the ground. That is all they show. I have not identified any of them as a specific quarry from the historical record, and I have not counted how many candidates were right and how many were wrong. There are still no accuracy numbers, and two days of photographs would never give me any.

But something did change for me on that trip, and it is not a number. Walking to a point because a satellite told me to look there is a very different experience from wandering around and finding a pond by accident. In March, the island showed me what it wanted to show me. In August, I arrived with a list. That list came out of open data and open-source code, and that is the part of this work that travels to other places.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 8月31日に再訪。これは現地確認の開始であって精度検証ではない。公開済み145件から座標・面積付きの候補リストを作り、面積順位より安全・立入許可・到達可能性を優先して訪問先を選んだ。写真は illustrative であり、丁場としての同定も正誤の集計も行っていない。3月は島が見せるものを見たが、8月はリストを持って行った。
- 写真が未撮影・差し替え前の場合は、このスライドを削除した11枚版を使う。既存写真での代替はしない。
- 「候補地点に水があった」といった正誤の含意を語らない。写真は候補地点の存在を示すのみ。
- サンプリング設計された accuracy validation ではないことを英語で必ず言う。

---

### Slide 10 — What this can and cannot tell you

**EN (spoken)**

Let me be explicit about where this breaks.

Ten metre resolution. A pond narrower than about ten metres is unreliable, and that island has narrow flooded cuts. Thresholds below zero. They let in dark rock and deep shadow, and that is the price I paid for keeping the small ponds. No precision and no recall, because the field validation that would produce those numbers has not been done.

And what I detect is water, not quarries. A natural pond is water. An irrigation reservoir is water. A water tank is water. Near the shoreline, a polygon can be partly sea. I have not separated any of those out.

One more, which I mentioned earlier. The vegetation mask removed only nine pixels. I had expected vegetation to be a real problem, and it was not, so my mental model of the failure mode was wrong.

The next steps are simple and boring. Walk the candidates. Add a land mask so the shoreline stops leaking in. Try higher-resolution imagery on the narrow ones. None of that needs a new method. It needs somebody to go and look.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 10 m解像度では約10 m未満の池は信頼できない。負の閾値は暗い岩肌や影を取り込む。精度指標はなく、現地検証も行っていない。検出しているのは水域であって丁場ではないため、自然の池・農業用ため池・貯水施設が含まれ得る。海岸線付近のポリゴンには海水が含まれる可能性がある。NDVIマスクの除外が9ピクセルのみだったことは、当初の想定が外れたことを示す。次の一手は候補の踏査・海岸線用の陸域マスク・高分解能画像。
- 限界は弁明せず短く言い切る。ここで補足を足すほど弱く聞こえる。
- 「今後の課題」を新手法の必要性として語らない。必要なのは現地確認である。

---

### Slide 11 — The 145 polygons are open data now

**EN (spoken)**

The 145 polygons are open data now. They are published as GeoJSON, in EPSG 4326, so you could open them in QGIS this afternoon if you wanted to.

Let me be precise about what is public. The detected polygons are public. The pipeline also writes raster output for fieldwork and heritage documentation, and that is an output format rather than something I have published.

The whole pipeline is open-source Python: rasterio, numpy, shapely, pystac-client, planetary-computer and folium. No licence fee. No imagery purchase.

Which means the same workflow could be extended to other quarried islands in the Seto Inland Sea, and there are several of them. One warning if you try it. Do not carry my thresholds across unchanged. They came out of the histogram of this island, in this season, in this water. Derive your own.

The imagery is modified Copernicus Sentinel data from 2025, and this work is CC BY 4.0.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 145件は GeoJSON（EPSG:4326）として公開済み。パイプラインは現地調査・遺産記録向けにラスタ出力も生成するが、こちらは出力仕様であって公開物ではない。実装はOSSのPythonのみ（rasterio, numpy, shapely, pystac-client, planetary-computer, folium）。ライセンス費・画像購入費は不要。瀬戸内の他の採石島へ展開可能だが、閾値はそのまま持ち込めない。
- 公開物（GeoJSON）とパイプライン出力（GeoTIFF）を混同しない。この区別を英語で必ず言う。
- 帰属表記（Copernicus・CC BY 4.0）はこことS6で口頭にも載せる。

---

### Slide 12 — Check them on the ground, then put them on the map

**EN (spoken)**

So here is the loop I would like to leave you with.

A satellite scan turns an unknown into a finite candidate list. A field visit turns a candidate into something you have seen with your own eyes. And OpenStreetMap is where what you confirmed stops being my private file and becomes a public map that anyone can use.

I plan to contribute the ponds I can confirm. I want to be clear that this is a plan. I have not done it yet, and I will only add the ones I have actually stood in front of.

In March, the mapping party added features observed on the ground. The scan suggests where to look next. That is the whole idea.

Thank you. I am happy to take questions.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 衛星で候補を絞る → 現地で自分の目で確かめる → 確かめたものを OpenStreetMap に載せる。この一巡を提案として置く。還元は今後の計画であり、まだ行っていない。追加するのは現地で確認できたものに限る。
- 「まだ地図にない」という欠落の指摘で終わらせない。前向きなループの提案で閉じる。
- OSMへの還元を既に行ったと述べない。この留保を英語で必ず言う。
