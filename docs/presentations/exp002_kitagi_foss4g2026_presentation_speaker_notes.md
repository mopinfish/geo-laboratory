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

Good afternoon. Please look at this wall. This cliff is not natural. People have quarried granite on this island for about four hundred years, and this wall is one result. The water at the bottom arrived later, after the cutting stopped. This is a photograph I took on the island myself. It is not a map, and it is not a result from my analysis. For the next twenty minutes I will show you the same island at three different scales.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 「この崖は自然のものではない」から入る。この島では約400年にわたり花崗岩が切り出されてきており、この壁はその結果のひとつ。水はその後に溜まったもの。写真は著者が現地で撮影したもので、検出結果の図ではない。
- 冒頭の一言は「この崖は自然のものではない」に固定する。ここで手法の話をしない。
- 氏名・所属は表紙に投影されているため口頭では述べない（発話は写真の説明に集中させる）。
- 表紙写真は現地写真。検出結果の可視化と誤解されないよう「結果ではない」と明言する。

---

### Slide 2 — A quarrying island, and the ponds it left behind

**EN (spoken)**

So, where are we? Kitagi Island sits in the Seto Inland Sea, in Kasaoka City, Okayama Prefecture. It is the largest of the Kasaoka Islands.

People have been cutting granite there since the early seventeenth century. At the peak, in 1957, the island had one hundred and twenty-seven active quarry sites, and up to twelve thousand people lived there. Today there are two working quarries, and about six to seven hundred residents.

Here is the part that matters for this talk. Many abandoned pits were not backfilled. Some of them accumulated rainwater and groundwater, and became ponds. So the island is left with a large number of flooded holes, in a landscape where people still live, still work, and still walk around.

In 2019 the island became national heritage, as one of the "Stone Islands of Setouchi". That designation has raised interest in the quarry landscape itself.

And that is where my problem started. I went looking for a list of the ponds. Where are they? How big are they? How many are there? I found no island-wide record of the ponds themselves.

I want to be careful with that sentence. It describes my search, not the world. Partial records do exist, and I will come back to them later in the talk. What I could not find was an inventory of the water bodies for the island as a whole.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 位置（瀬戸内海・岡山県笠岡市。笠岡諸島最大の島）、17世紀初頭からの採石、1957年ピークで127丁場・人口1万2千人、現在は稼働2丁場・住民600〜700人。廃止後の丁場は埋め戻されないものが多く、一部に雨水と地下水が溜まって池になった。2019年に日本遺産「石の島」認定により、丁場の景観そのものへの関心が高まった。島全体の池の記録は見つからなかった。
- 「見つからなかった」は**探索範囲の限定**であって、存在しないという断定ではない。この留保を英語で必ず言う。
- オープンデータに部分的な記録があることはS8で参考として触れる。ここでは「後で戻る」とだけ言う。
- 石材の用途（城壁・橋・著名建築）は権威資料に含まれていないため語らない。

---

### Slide 3 — On foot: I could stand in front of five or six of them

**EN (spoken)**

My own story with the island starts in March this year, at a drone mapping party. A group of people who like maps came over for two days, to fly drones and to add what we saw to the map.

Walking around, the first thing you notice is the walls. They are vertical, and they are flat, and they are clearly cut rather than weathered. You can still read the lines where the stone was split.

The second thing you notice is the water. It is green — a deep, unusual green. The published descriptions give depths from a few metres to about twenty metres. That figure comes from the record, not from anything I measured. Standing at the edge, you believe it.

And then there is the stage. One of the flooded quarries has a small wooden stage built out on the water. In front of it, blocks of stone are laid out as seats. The island sometimes uses the place as a venue for events.

Now, the important number on this slide is a small one. I visited five or six quarry sites during the two-day event, on foot or by car. It felt like a lot at the time. Please remember that number, because it comes back later, and it is really the reason this talk exists.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 2026年3月のドローン・マッピングパーティ参加が出発点。垂直で平らな切削面、深く独特な緑の水面、数メートル〜約20メートルとされる水深、湖上に設えられた木製の小さなステージと、座席代わりに並べられた石（湖上イベントの会場として使われることがある）。イベント中に訪れたのは徒歩または車で5〜6か所。
- 水深は報告書由来の記述であり著者の計測値ではない。英語でも "from the record, not from anything I measured" と必ず言う。
- 徒歩スケールで分かるのは**質感**だけ。島全体は見えないという流れをS7へつなぐ。
- 「5〜6か所」はS8の規模対比の伏線。ここで数字を印象づける。移動手段は徒歩または車であり、訪問先を検出ポリゴンへ照合したものでもない。

---

### Slide 4 — From the air: the quarry boundaries are the landform

**EN (spoken)**

On the second day we flew from the stage on the water. And the island changed shape.

From the air, the quarries read as grey rectangles cut into a green canopy. Straight edges, right angles, sharp corners. Nothing else on that island looks like that.

The thing I did not expect is what sits between them. Two companies once held quarrying rights side by side. Neither company cut through the boundary. So a thin wall of granite is left standing between the two pits. A property line, standing as terrain. A line on a legal document became a landform.

You cannot see that from the ground, because you are inside one pit or the other. And from orbit, at ten metres, the wall is too thin to notice. You can only see it from the air.

I should be clear that this is me looking and describing. It is a qualitative observation from that day, not a measurement from this study. We also flew a survey over one of the lakes while we were there.

And one more thing from those two days, which I will pick up again at the end. The same event added features to OpenStreetMap. We put on the map the things we could see on the ground, but that did not create an island-wide inventory.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 2日目に湖上ステージからドローンを飛ばした。上空からは緑の樹冠に切り込まれた灰色の矩形として見える。かつて2社が隣り合って採石権を持っていたが、どちらもその境界を切り崩さなかったため、細い花崗岩の壁として残っている。所有権の線が地形になっている。イベントではOpenStreetMapへの地物追加と湖の測量も行った。
- 境界が地形になっているという観察は**現地での定性的観察**であり、本研究の測定結果ではない。英語でも明言する。
- イベントで追加したのは現地で観察できた地物のみ。徒歩到達範囲を網羅的に地図化したとは述べない。
- 最後の一文（島全体のインベントリにはなっていない）はS12の「地図に還す」への伏線。

---

### Slide 5 — On the train home: one satellite scene covers the whole island

**EN (spoken)**

On the train home, I was still thinking about the five or six quarry sites I had visited — and how little of the island I had seen. There is one instrument that covers the whole island in a single frame, and it is free to use.

I downloaded a Sentinel-2 Level-2A scene through the STAC API of the Microsoft Planetary Computer. The summer scene is from the second of August 2025, with zero point seven percent cloud, on a ten metre grid.

I want to say clearly that this is a standard water-index workflow; the method is not new. All three indices are simple band arithmetic. NDWI compares green and near-infrared light. MNDWI compares green and short-wave infrared. NDVI compares near-infrared and red. Either water index can flag a pixel. NDVI then removes pixels marked as vegetation. The exact expression is on the slide. The two water cut-offs sit just below zero — minus zero point two, and minus zero point one. The vegetation cut-off is zero point three.

You may be wondering why two of those thresholds sit below zero. The reason is the pixel size. At ten metres, a narrow pond is part water, part granite and part shadow, all inside one pixel, so a strict positive threshold can miss small ponds or mixed shoreline pixels.

I picked the numbers from the valley in the histogram. I did not optimise them, I did not run a sensitivity analysis, and I did not check them in the field. The short-wave band arrives at twenty metres, so I resampled it to ten. And I only report polygons of one hundred square metres or more.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: Sentinel-2 L2A のシーンを Microsoft Planetary Computer の STAC API 経由でダウンロードした。2025年8月2日・雲量0.7%・10 m グリッド。NDWI＝緑と近赤外、MNDWI＝緑と短波赤外、NDVI＝近赤外と赤。水域条件は（NDWI > −0.2 または MNDWI > −0.1）かつ NDVI > 0.3 でない。負の閾値は10 mでの混合画素への対処。閾値はヒストグラムの谷から決めた値で、最適化・感度分析・現地検証はしていない。短波赤外は20 mから10 mへリサンプリング。報告下限は100 m²。
- 3指数の**式は投影本文に置かず図版の中に置く**。したがって「何と何から作るか」は英語の発話で必ず言う。閾値そのものはスライドに出ているので、口頭では式を読み上げず規則の形だけを言い、数値は一度だけ落ち着いて言う。指数の説明は1文1指数の短文に分けてあるので、続けて速く読まず、指数ごとに区切る。
- `STAC` は一語として読まず、`S-T-A-C` と1文字ずつ読む。
- 「標準的な手順であり手法の新規性はない」も英語で必ず言う。本発表は手法の新規性を主張しない。
- 閾値の由来（ヒストグラムの谷・最適化なし）はこのスライドの留保。急いでいても削らない。

---

### Slide 6 — The scan found 145 water polygons across the island

**EN (spoken)**

So: one scene, one island, and this is what came out. The scan found one hundred and forty-five water polygons inside the island, each at least one hundred square metres.

There are two scenes behind this. For spring, I used a scene from the twenty-third of March 2025. Its reported cloud cover was zero point zero percent. We reported one hundred and thirteen polygons. The largest was one point two eight hectares. The summer scene was from the second of August 2025, with zero point seven percent cloud. It returned one hundred and forty-five polygons. The largest was seven thousand eight hundred and twenty-six square metres.

Now the honest part. The two reported scenes differed, but we have not isolated the cause. It is tempting to say this is the season, and I am not going to say that. The spring figure is what we reported; that run's configuration is not preserved. So please treat one hundred and thirteen as the reported value, with a reproducibility limitation.

One result did surprise me. I put the vegetation index into the rule because I expected green water and green canopy to be confused. The NDVI vegetation mask removed only nine pixels. Nine. It added little to this particular result, and I would rather say so than leave it out.

Now look at where the polygons are. They cluster in the north, the south-east, the centre and the west — where the historical records put the quarrying. At the peak in 1957 the island had one hundred and twenty-seven recorded quarry sites. My scan returned one hundred and forty-five detections. Those two numbers are close, and I want to be careful here. This is a comparison of scale, and not a one-to-one match. I have not matched any detection to an individual quarry, and I am not claiming that I can.

The line at the bottom of the slide is the one to take away. These are detected water polygons, not individually field-confirmed quarry ponds. I have no precision figure and no recall figure, because I have not done the field validation that would produce them. The imagery is modified Copernicus Sentinel data from 2025.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 夏季シーンから島内145件（各100 m²以上）を検出。春季 2025-03-23・報告雲量0.0%・報告113件・最大1.28 ha、夏季 2025-08-02・雲量0.7%・145件・最大7,826 m²。両者は差があるが原因は特定できていない。春季値は当時の報告値で実行設定が保存されていない。NDVIマスクの除外は9ピクセルのみ（この結果への寄与は小さかった）。分布は北・南東・中央・西の4集中帯で歴史記録と整合。145対127は規模の比較であって1対1対応ではない。検出は候補であり個別に現地確認されていない。精度指標は算出していない。
- 春季113は当時の報告値であり、現行パイプラインで同一シーンを再計算すると180件になる（113は未再現）。この数はスライドにも英語の発話にも出さないが、再現性を問われた場合に答えられるよう把握しておく。
- 必須発話6行（両シーンの日付・雲量・件数・最大面積、原因未特定、実行設定の非保存、NDVIの9ピクセル、候補であって現地確認済みでない旨）はこのスライドの契約事項。時間が押しても削らない。
- 雲量は「報告値（reported cloud cover）」として数値で述べる。「雲がまったく無かった」のような見た目の印象に置き換えない。
- 数値は1文1項目に分けてある。7,826 m²（seven thousand eight hundred and twenty-six square metres）の前後では一拍置き、桁を潰さずに言う。
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

None of these three is better than the others. Not better or worse — different things become visible. And if you only ever work at one scale, you may be seeing only part of the problem.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 徒歩＝質感、上空＝境界、衛星＝分布。三つは優劣ではなく別のものを見せる。ひとつの縮尺だけで作業すると、問題の一部しか見えていない可能性がある。
- 本スライドは解釈の提示であり、新しい数値は出さない。
- 「145 candidates」と言う（detections でも可だが、丁場数と読める言い方はしない）。

---

### Slide 8 — Five or six sites visited — the scan produced 145 candidates

**EN (spoken)**

Now I want to hold two numbers against each other, because the gap between them is the whole point of the talk. During the mapping party I stood in front of five or six quarry sites. From a single satellite scene I got one hundred and forty-five water polygons.

I am not saying that my five or six are five or six of the 145. I never matched the places I visited to individual polygons, so please hear this as a contrast of scale and nothing more. Individual ponds are not field-confirmed. There is no precision and no recall yet.

One reference point: every OpenStreetMap quarry feature in the comparison overlapped a detection. I pulled that comparison in late August, and I am showing it only as a reference. But OpenStreetMap is not ground truth, and overlap does not prove identity. So I will not call it agreement, and I do not report it as accuracy.

Before the scan, the honest answer I could find to "how many drowned quarries are on this island" was that there is no public island-wide list. Nor does the scan tell us how many drowned quarries exist. It gives 145 water-polygon candidates to prioritise, subject to access, safety and permission. That finite list makes fieldwork possible to plan.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 訪問5〜6か所に対し、1シーンから145件の検出。訪問地点を個別ポリゴンに照合した記録はないため、これは規模の対比にとどまる。個別の池は現地確認されておらず、精度指標もない。参考として、比較対象としたOSMの丁場地物はいずれも検出と重なった（照合は8月下旬）。ただしOSMは正解データではなく、重なりは同一地物であることの証明にはならないため、精度としては報告しない。走査の前に見つけられた答えは「島全体を網羅した公開リストは無い」であり、走査もまた丁場池の総数を教えてはくれない。得られるのは、立入可否・安全・許可を前提に優先順位を付けるための水域ポリゴン候補145件であり、この有限のリストが現地調査の計画を可能にする。
- OSMは参考値。件数の内訳・距離の定義・感度は投影せず、口頭でも数値化しない（質疑で聞かれた場合のみ想定問答で答える）。
- 訪問地点が検出集合の部分集合であるとは主張しない。この否定を英語で必ず言う。
- 到達可能性は安全・立入許可に依存する。「歩けば全部確認できる」とは言わない。

---

### Slide 9 — Two days ago I went back — a first look, not validation

**EN (spoken)**

This slide is about the return visit to the island, on the thirty-first of August. I want to be very clear about what it is and what it is not. It is a first look. It is not validation.

Here is how I choose where to go. The published set of one hundred and forty-five polygons carries a coordinate and an area for every candidate, so a short list is easy to build. But area ranking is not what decides the route. On a working quarry island, safety, permission, and simply being able to walk to a place matter more than which pond is the largest. So these points are not a sample designed for accuracy. They are candidates selected for an attempted field visit.

The photographs in these slots are there to illustrate the candidates, not to validate accuracy. They are meant to show what the scan pointed at, seen from the ground, and nothing beyond that. No candidate here is identified as a specific quarry from the historical record, and there is no count of how many candidates were right and how many were wrong. There are no accuracy numbers on this slide, and a day of photographs would never produce any.

What a visit like this changes is not a number. Walking to a place because a satellite pointed at it is a very different way of working from wandering around and finding a pond by accident. In March, the island decided what I saw. This time the list comes first, and the list comes out of open data and open-source code. That is the part of this work that travels to other islands.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 8月31日の再訪スライド。これは現地確認の開始であって精度検証ではない。公開済み145件は各候補の座標と面積を持つため候補リストは容易に作れるが、訪問先は面積順位ではなく安全・立入許可・到達可能性で決める。これらは訪問を試みる対象として選んだ候補であり、到達できることが事前に確認されているわけではない。写真は illustrative であり、候補を歴史記録上の丁場として同定するものでも、正誤を集計するものでもない。3月は島が見せるものを見たが、今回はリストが先にある。
- **[UPDATE AFTER 2026-08-31]** 再訪の実施後にこのスライドを見直す。英語本文は再訪前に書いたため、まだ起きていない出来事・情景・感想を語らず、候補の選び方と写真が示す範囲、そして留保だけで構成してある。写真が確定したら、実際に写っているものに合わせて英語本文を書き直す。
- 写真が未撮影・差し替え前の場合は、このスライドを削除した11枚版を使う。既存写真での代替はしない。
- 「候補地点に水があった」といった正誤の含意を語らない。写真は候補地点の存在を示すのみ。
- サンプリング設計された accuracy validation ではないことを英語で必ず言う。

---

### Slide 10 — What this can and cannot tell you

**EN (spoken)**

Before I take this any further, I should be explicit about its limits.

Ten metre resolution. A pond narrower than about ten metres is unreliable, and that island has narrow flooded cuts. Thresholds below zero. They let in dark rock and deep shadow, and that is the price I paid for keeping the small ponds. No precision and no recall, because the field validation that would produce those numbers has not been done.

And what I detect is water, not quarries. A natural pond is water. An irrigation reservoir is water. A water tank is water. Near the shoreline, a polygon can be partly sea. I have not separated any of those out.

One more, which I mentioned earlier. I had expected vegetation to be a real problem. The mask changed only nine pixels in this run, so it added little to this particular result.

The next steps are straightforward, but essential. Walk the candidates. Add a land mask so the shoreline stops leaking in. Try higher-resolution imagery on the narrow ones. None of that needs a new method. It needs somebody to go and look.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: 10 m解像度では約10 m未満の池は信頼できない。負の閾値は暗い岩肌や影を取り込む。精度指標はなく、現地検証も行っていない。検出しているのは水域であって丁場ではないため、自然の池・農業用ため池・貯水施設が含まれ得る。海岸線付近のポリゴンには海水が含まれる可能性がある。NDVIマスクの除外はこの実行では9ピクセルのみで、この結果への寄与は小さかった。次の一手は候補の踏査・海岸線用の陸域マスク・高分解能画像。
- 限界は弁明せず短く言い切る。ここで補足を足すほど弱く聞こえる。
- 冒頭は「次に進む前に限界を明示する」という前置きで入る。11枚版（S9なしでS8の直後）でもそのまま成立する言い方にしてある。
- 「次の一手」は退屈な作業としてではなく、簡明だが不可欠な作業として述べる。
- 「今後の課題」を新手法の必要性として語らない。必要なのは現地確認である。

---

### Slide 11 — The 145 polygons are open data now

**EN (spoken)**

To make that next step possible, the 145 polygons are open data now. They are published as GeoJSON, in EPSG 4326, so you could open them in QGIS this afternoon if you wanted to.

Now, what exactly is public? The detected polygons are public. The pipeline also writes raster output for fieldwork and heritage documentation, and that is an output format rather than something I have published.

The pipeline uses open-source Python libraries, including Rasterio, NumPy and Shapely. There are no licence fees and no imagery to buy.

Which means the same workflow could be extended to other quarried islands in the Seto Inland Sea, and there are several of them. One warning if you try it. Do not carry my thresholds across unchanged. They came out of the histogram of this island, in this season, in this water. Derive your own.

The imagery is modified Copernicus Sentinel data from 2025, and this work is CC BY 4.0.

**JA (not spoken)** — 訳と補足。読み上げない。

- 訳: S10の「見に行く」を可能にするために、145件は GeoJSON（EPSG:4326）として公開済み。パイプラインは現地調査・遺産記録向けにラスタ出力も生成するが、こちらは出力仕様であって公開物ではない。実装はOSSのPythonライブラリのみで、口頭ではrasterio・numpy・shapelyの3つだけを挙げる（6つの全リストはフッターに投影されている）。ライセンス費・画像購入費は不要。瀬戸内の他の採石島へ展開可能だが、閾値はそのまま持ち込めない。
- 公開物（GeoJSON）とパイプライン出力（GeoTIFF）を混同しない。この区別を英語で必ず言う。
- ライブラリ名の6連続は口頭では潰れるため、発話は3つに絞る。残りはフッターの投影で足りる。
- `EPSG 4326` に触れる場合は `E-P-S-G four three two six` と1文字ずつ読む。
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
