# FOSS4G 2026 Hiroshima 口頭発表 スピーカーノート（英語原稿・日本語原稿・非発話の補足）

会場が求めている発話言語は**英語**である（採択通知に明記されている）。壇上で読むのは
`EN (spoken)` の英語原稿である。

`JA（訳・読み上げ可）` の日本語は、**練習・自己確認・万一の代替**のために、そのまま
声に出して読める発表原稿として書いてある。英語と同じ内容・同じ留保を運ぶ。英日を
交互に話す二言語進行のための原稿ではない。

`JA（補足・読み上げない）` には、主張境界・言い回しの注意・伏線の申し送りを置く。
ここは壇上で声に出さない。日本語原稿を頭から末尾まで読み上げても、非発話の内容が
口から出ない構造にしてある。

各スライドの英語は、発表時間の割り当て（合計1,050秒）を 145 wpm で換算した語数を目安に
している。日本語原稿は同じ秒数を 300〜350 字/分で換算した文字数（空白・改行を除く）を
目安にしている。通し読みで押している場合は、数値と留保（候補である旨・精度指標の不在・
春季値の由来）を残したまま、情景描写の側から削る。

同じ内容が PPTX のノートペインにも入っている（英語原稿 → 日本語原稿 → 非発話の補足の順）。

---

### Slide 1 — Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

**EN (spoken)**

Good afternoon. Please look at this wall. This cliff is not natural. People have quarried granite on this island for about four hundred years, and this wall is one result. The water at the bottom arrived later, after the cutting stopped. This is a photograph I took on the island myself. It is not a map, and it is not a result from my analysis. For the next twenty minutes I will show you the same island at three different scales.

**JA（訳・読み上げ可）**

こんにちは。まず、この壁を見てください。この崖は自然のものではありません。この島では約400年にわたって花崗岩が切り出されてきました。この壁はその結果のひとつです。底に見える水は、切り出しが止まったあとに溜まったものです。これは私が島で自分で撮った写真です。地図ではありませんし、私の分析の結果でもありません。これから20分間、同じ島を三つの違う縮尺でお見せします。

**JA（補足・読み上げない）**

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

**JA（訳・読み上げ可）**

では、どこの話でしょうか。北木島は瀬戸内海にあります。岡山県笠岡市の島で、笠岡諸島でいちばん大きな島です。

この島では17世紀の初めから花崗岩が切り出されてきました。ピークは1957年です。そのとき島には127か所の稼働中の丁場があり、多いときには1万2千人が暮らしていました。今も稼働しているのは2か所で、住民は600人から700人ほどです。

ここからがこの発表に関わる部分です。採石をやめた穴の多くは、埋め戻されませんでした。そのいくつかに雨水と地下水が溜まり、池になりました。つまりこの島には、水の溜まった穴がたくさん残っています。しかもそこは、今も人が住み、働き、歩いている場所です。

2019年、この島は「石の島」として日本遺産になりました。この認定で、丁場の景観そのものへの関心が高まりました。

私の問題はそこから始まりました。私は池のリストを探しました。どこにあるのか。どれくらいの大きさなのか。いくつあるのか。島全体をまとめた池の記録は、見つかりませんでした。

この言い方には気をつけたいです。これは私の探し方についての話で、世界についての話ではありません。部分的な記録は存在します。それにはあとで戻ってきます。私が見つけられなかったのは、島全体をひとまとまりとして扱った水域の目録です。

**JA（補足・読み上げない）**

- 「見つからなかった」は**探索範囲の限定**であって、存在しないという断定ではない。この留保を英語で必ず言う。
- オープンデータに部分的な記録があることは後半で参考として触れる。ここでは「あとで戻る」とだけ言う。
- 石材の用途（城壁・橋・著名建築）は権威資料に含まれていないため語らない。

---

### Slide 3 — On foot: I could stand in front of five or six of them

**EN (spoken)**

My own story with the island starts in March this year, at a drone mapping party. A group of people who like maps came over for two days, to fly drones and to add what we saw to the map.

Walking around, the first thing you notice is the walls. They are vertical, and they are flat, and they are clearly cut rather than weathered. You can still read the lines where the stone was split.

The second thing you notice is the water. It is green — a deep, unusual green. The published descriptions give depths from a few metres to about twenty metres. That figure comes from the record, not from anything I measured. Standing at the edge, you believe it.

And then there is the stage. One of the flooded quarries has a small wooden stage built out on the water. In front of it, blocks of stone are laid out as seats. The island sometimes uses the place as a venue for events.

Now, the important number on this slide is a small one. I visited five or six quarry sites during the two-day event, on foot or by car. It felt like a lot at the time. Please remember that number, because it comes back later, and it is really the reason this talk exists.

**JA（訳・読み上げ可）**

私自身とこの島の話は、今年の3月に始まります。きっかけはドローン・マッピングパーティでした。地図が好きな人たちが二日間集まって、ドローンを飛ばし、見たものを地図に足す催しです。

歩いてまず目に入るのは壁です。垂直で、平らで、風化ではなく切られた面だとすぐ分かります。石を割った線も、今も読み取れます。

次に目に入るのは水です。緑色です。深く、独特な緑です。公開されている記述では、水深は数メートルから20メートルほどとされています。この数字は記録によるもので、私が測ったものではありません。ふちに立つと、その数字を信じられます。

それからステージです。水没した丁場のひとつには、水の上に小さな木のステージが作られています。その前には、石の塊が客席のように並べられています。島ではこの場所を催しの会場として使うこともあります。

このスライドで大事な数字は、小さな数字です。私はこの二日間の催しで、5か所か6か所の丁場を訪れました。徒歩か車です。そのときは、たくさん見たつもりでした。この数字を覚えておいてください。あとでまた出てきます。この発表があるのは、本当にこの数字のためです。

**JA（補足・読み上げない）**

- 水深は報告書由来の記述であり著者の計測値ではない。英語でも "from the record, not from anything I measured" と必ず言う。
- 徒歩スケールで分かるのは**質感**だけ。島全体は見えないという流れを三スケールのスライドへつなぐ。
- 「5〜6か所」は後半の規模対比の伏線。ここで数字を印象づける。移動手段は徒歩または車であり、訪問先を検出ポリゴンへ照合したものでもない。

---

### Slide 4 — From the air: the quarry boundaries are the landform

**EN (spoken)**

On the second day we flew from the stage on the water. And the island changed shape.

From the air, the quarries read as grey rectangles cut into a green canopy. Straight edges, right angles, sharp corners. Nothing else on that island looks like that.

The thing I did not expect is what sits between them. Two companies once held quarrying rights side by side. Neither company cut through the boundary. So a thin wall of granite is left standing between the two pits. A property line, standing as terrain. A line on a legal document became a landform.

You cannot see that from the ground, because you are inside one pit or the other. And from orbit, at ten metres, the wall is too thin to notice. You can only see it from the air.

I should be clear that this is me looking and describing. It is a qualitative observation from that day, not a measurement from this study. We also flew a survey over one of the lakes while we were there.

And one more thing from those two days, which I will pick up again at the end. The same event added features to OpenStreetMap. We put on the map the things we could see on the ground, but that did not create an island-wide inventory.

**JA（訳・読み上げ可）**

二日目、私たちは水上のステージからドローンを飛ばしました。すると、島の形が変わって見えました。

上空から見ると、丁場は緑の樹冠に切り込まれた灰色の四角形として読めます。まっすぐな縁、直角、とがった角。この島で、こんな形のものは他にありません。

思っていなかったのは、その間にあるものです。かつて2つの会社が、隣り合って採石の権利を持っていました。どちらも、その境目を切り崩しませんでした。だから2つの穴の間には、細い花崗岩の壁が立ったまま残っています。所有の境界線が、地形として立っています。書類の上の線が、地形になったのです。

これは地上からは見えません。自分はどちらかの穴の中にいるからです。軌道上からも見えません。10メートルでは、壁が細すぎて気づけません。見えるのは上空からだけです。

これは私が見て述べていることです。その日の定性的な観察であって、この研究の測定結果ではありません。あの日は、湖の上で測量の飛行もしました。

もうひとつ、あの二日間のことを最後にまた取り上げます。同じ催しで、OpenStreetMap に地物を追加しました。地上で見えたものを地図に載せたのです。ただ、それで島全体の目録ができたわけではありません。

**JA（補足・読み上げない）**

- 境界が地形になっているという観察は**現地での定性的観察**であり、本研究の測定結果ではない。英語でも明言する。
- イベントで追加したのは現地で観察できた地物のみ。徒歩到達範囲を網羅的に地図化したとは述べない。
- 最後の一文（島全体のインベントリにはなっていない）は、最終スライドの「地図に還す」への伏線。

---

### Slide 5 — On the train home: one satellite scene covers the whole island

**EN (spoken)**

On the train home, I was still thinking about the five or six quarry sites I had visited — and how little of the island I had seen. There is one instrument that covers the whole island in a single frame, and it is free to use.

I downloaded a Sentinel-2 Level-2A scene through the STAC API of the Microsoft Planetary Computer. The summer scene is from the second of August 2025, with zero point seven percent cloud, on a ten metre grid.

I want to be clear about one thing: this is a standard water-index workflow, and the method is not new. All three indices are simple band arithmetic. NDWI compares green and near-infrared light. MNDWI compares green and short-wave infrared. NDVI compares near-infrared and red. Either water index can flag a pixel. NDVI then removes pixels marked as vegetation. The exact expression is on the slide. The two water cut-offs sit just below zero — minus zero point two, and minus zero point one. The vegetation cut-off is zero point three.

You may be wondering why two of those thresholds sit below zero. The reason is the pixel size. At ten metres, a narrow pond is part water, part granite and part shadow, all inside one pixel, so a strict positive threshold can miss small ponds or mixed shoreline pixels.

I picked the numbers from the valley in the histogram. I did not optimise them, I did not run a sensitivity analysis, and I did not check them in the field. The short-wave band arrives at twenty metres, so I resampled it to ten. And I only report polygons of one hundred square metres or more.

**JA（訳・読み上げ可）**

帰りの電車でも、訪れた5、6か所のことを考えていました。島のほんの一部しか見ていない、とも考えていました。島全体を一枚の画像で覆える装置があります。しかも無料です。

Sentinel-2 の Level-2A のシーンを、Microsoft Planetary Computer の STAC API から取りました。夏のシーンは2025年8月2日、雲量0.7パーセント、格子10メートルです。

はっきりさせます。これは水域指数を使った標準的な手順で、手法として新しいところはありません。3つの指数はどれも単純なバンド演算です。NDWI は緑と近赤外を比べます。MNDWI は緑と短波赤外を比べます。NDVI は近赤外と赤を比べます。水域指数は、どちらか一方でも画素を水として拾えます。そこから NDVI が、植生と印のついた画素を外します。式はスライドに出ています。水域側の閾値は2つとも、ゼロを少し下回ります。マイナス0.2とマイナス0.1です。植生側は0.3です。

なぜゼロを下回るのか、気になると思います。理由は画素の大きさです。10メートルでは、細い池は一部が水、一部が花崗岩、一部が影で、一つの画素に混ざります。正の側で厳しく切ると、小さな池や岸際の混ざった画素を落とします。

数値はヒストグラムの谷から選びました。最適化も感度分析もしていません。現地で確かめてもいません。短波赤外のバンドは20メートルで届くので、10メートルにリサンプリングしました。報告するのは100平方メートル以上のポリゴンだけです。

**JA（補足・読み上げない）**

- 3指数の**式は投影本文に置かず図版の中に置く**。したがって「何と何から作るか」は英語の発話で必ず言う。閾値そのものはスライドに出ているので、口頭では式を読み上げず規則の形だけを言い、数値は一度だけ落ち着いて言う。指数の説明は1文1指数の短文に分けてあるので、続けて速く読まず、指数ごとに区切る。
- `STAC` は一語として読まず、`S-T-A-C` と1文字ずつ読む。
- 「標準的な手順であり手法の新規性はない」も英語で必ず言う。本発表は手法の新規性を主張しない。
- 閾値の由来（ヒストグラムの谷・最適化なし）はこのスライドの留保。急いでいても削らない。
- B11（短波赤外）は 20 m から 10 m へのリサンプリングであることを、質疑で問われたら答える。

---

### Slide 6 — The scan found 145 water polygons across the island

**EN (spoken)**

So: one scene, one island, and this is what came out. The scan found one hundred and forty-five water polygons inside the island, each at least one hundred square metres.

There are two scenes behind this. For spring, I used a scene from the twenty-third of March 2025. Its reported cloud cover was zero point zero percent. We reported one hundred and thirteen polygons. The largest was one point two eight hectares. The summer scene was from the second of August 2025, with zero point seven percent cloud. It returned one hundred and forty-five polygons. The largest was seven thousand eight hundred and twenty-six square metres.

Now the honest part. The two reported scenes differed, but we have not isolated the cause. It is tempting to say this is the season, and I am not going to say that. The spring figure is what we reported; that run's configuration is not preserved. So please treat one hundred and thirteen as the reported value, with a reproducibility limitation.

One result did surprise me. I put the vegetation index into the rule because I expected green water and green canopy to be confused. The NDVI vegetation mask removed only nine pixels. Nine. It added little to this particular result, and I would rather say so than leave it out.

Now look at where the polygons are. They cluster in the north, the south-east, the centre and the west — where the historical records put the quarrying. At the peak in 1957 the island had one hundred and twenty-seven recorded quarry sites. My scan returned one hundred and forty-five detections. Those two numbers are close, and I want to be careful here. This is a comparison of scale, and not a one-to-one match. I have not matched any detection to an individual quarry, and I am not claiming that I can.

The line at the bottom of the slide is the one to take away. These are detected water polygons, not individually field-confirmed quarry ponds. I have no precision figure and no recall figure, because I have not done the field validation that would produce them. The imagery is modified Copernicus Sentinel data from 2025.

**JA（訳・読み上げ可）**

ひとつのシーン、ひとつの島。出てきたのがこれです。この走査は、島の中で145件の水域ポリゴンを見つけました。どれも100平方メートル以上です。

背後には2つのシーンがあります。春は、2025年3月23日のシーンを使いました。報告されている雲量は0.0パーセントでした。私たちが報告したのは113件です。最大は1.28ヘクタールでした。夏のシーンは2025年8月2日で、雲量は0.7パーセントです。返ってきたのは145件でした。最大は7,826平方メートルでした。

ここからは正直な話です。報告した2つのシーンには差がありました。ただ、その原因は特定できていません。季節のせいだと言いたくなりますが、私はそう言いません。春の数字は当時報告した値です。その実行の設定は保存されていません。ですから113件は、再現性に限界のある報告値として受け取ってください。

ひとつ、意外な結果がありました。緑の水面と緑の樹冠が混同されると考えて、私は植生指数を条件に入れました。ところが NDVI の植生マスクが外したのは、9画素だけでした。9画素です。この結果に足したものはほとんどありませんでした。黙っておくよりは、そう言いたいです。

ポリゴンがどこにあるかを見てください。北、南東、中央、西に固まっています。歴史の記録が採石の場所として挙げているところです。1957年のピークには、島に127か所の丁場が記録されていました。私の走査が返したのは145件の検出です。この2つの数字は近いのですが、ここは慎重に言います。これは規模の比較であって、1対1の対応ではありません。私はどの検出も個別の丁場に対応づけていませんし、対応づけられると主張してもいません。

持ち帰っていただきたいのは、スライドの下の一行です。これらは検出された水域ポリゴンであって、一件ずつ現地で確認された丁場池ではありません。適合率も再現率も出していません。それを出すための現地検証をしていないからです。画像は、2025年の Copernicus Sentinel データを加工したものです。

**JA（補足・読み上げない）**

- 春季113は当時の報告値であり、現行パイプラインで同一シーンを再計算すると180件になる（113は未再現）。この数はスライドにも英語の発話にも日本語の発話にも出さないが、再現性を問われた場合に答えられるよう把握しておく。
- 必須発話6行（両シーンの日付・雲量・件数・最大面積、原因未特定、実行設定の非保存、NDVIの9ピクセル、候補であって現地確認済みでない旨）はこのスライドの契約事項。時間が押しても削らない。
- 雲量は「報告値（reported cloud cover）」として数値で述べる。「雲がまったく無かった」のような見た目の印象に置き換えない。
- 数値は1文1項目に分けてある。7,826 m²（seven thousand eight hundred and twenty-six square metres）の前後では一拍置き、桁を潰さずに言う。
- 季節を原因として断定しない。「原因は特定できていない」で止める。
- 145件は検出数であって丁場数ではない。127との近さを一致として語らない。
- このスライド単体で2:30以内に収める。押している場合は情景描写ではなく分布の説明を短くする。

---

### Slide 7 — Each scale shows what the others cannot

**EN (spoken)**

Let me stop for a moment and put the three scales next to each other, because I think this is the real lesson from the island.

On foot I got texture. The cut face, the green water, the sense of depth. I could touch the rock. But I could only stand in one place at a time.

From the air I got boundaries. I could see that the line between two companies is a wall of rock, left standing. That is invisible from the ground, and it is too thin to matter from orbit.

From orbit I got distribution. One hundred and forty-five candidates, across the whole island, from a single frame. But at ten metres I cannot tell you whether a wall was cut or weathered.

None of these three is better than the others. Not better or worse — different things become visible. And if you only ever work at one scale, you may be seeing only part of the problem.

**JA（訳・読み上げ可）**

ここで少し立ち止まって、三つの縮尺を並べさせてください。これがこの島から得られる本当の教訓だと思うからです。

歩いて得られたのは質感です。切られた面、緑色の水、そして深さの感じです。岩に触ることもできました。ただ、一度に立てるのは一か所だけです。

上空から得られたのは境界です。2つの会社の間の線が、立ったまま残された岩の壁だと分かりました。それは地上からは見えません。そして軌道上からは、細すぎて意味を持ちません。

軌道上から得られたのは分布です。一枚の画像から、島全体で145件の候補が出ました。ただ10メートルでは、壁が切られたものなのか、風化したものなのかは分かりません。

この三つに優劣はありません。良い悪いではなく、見えるものが違うのです。そして、いつもひとつの縮尺だけで作業していると、問題の一部しか見ていないかもしれません。

**JA（補足・読み上げない）**

- 本スライドは解釈の提示であり、新しい数値は出さない。
- 「145 candidates」と言う（detections でも可だが、丁場数と読める言い方はしない）。

---

### Slide 8 — Five or six sites visited — the scan produced 145 candidates

**EN (spoken)**

Now I want to hold two numbers against each other, because the gap between them is the whole point of the talk. During the mapping party I stood in front of five or six quarry sites. From a single satellite scene I got one hundred and forty-five water polygons.

I am not saying that my five or six are five or six of the 145. I never matched the places I visited to individual polygons, so please hear this as a contrast of scale and nothing more. Individual ponds are not field-confirmed. There is no precision and no recall yet.

One reference point: every OpenStreetMap quarry feature in the comparison overlapped a detection. I pulled that comparison in late August, and I am showing it only as a reference. But OpenStreetMap is not ground truth, and overlap does not prove identity. So I will not call it agreement, and I do not report it as accuracy.

Before the scan, I went looking for an answer to a simple question: how many drowned quarries are on this island? The honest answer I could find was that there is no public island-wide list. Nor does the scan tell us how many drowned quarries exist. It gives 145 water-polygon candidates to prioritise, subject to access, safety and permission. That finite list makes fieldwork possible to plan.

**JA（訳・読み上げ可）**

2つの数字を並べます。この差がこの発表の主題だからです。マッピングパーティで、5、6か所の丁場の前に立ちました。衛星の1シーンからは、145件の水域ポリゴンが出ました。

ただ、私が見た5、6か所が145件のうちの5、6件だと言っているのではありません。訪れた場所を個別のポリゴンに対応づけたことはありません。ですからこれは規模の対比にすぎません。個々の池は現地で確認されていません。適合率も再現率も、まだありません。

参考として一点だけ。比較した OpenStreetMap の丁場の地物は、いずれも検出と重なっていました。比較は8月の下旬に取ったもので、参考にすぎません。ただ OpenStreetMap は正解データではありません。重なっても、同じ地物だとは証明できません。ですから一致とは呼びませんし、精度としても報告しません。

走査の前、この島に水没した丁場がいくつあるかを探しました。見つけられた正直な答えは、島全体を網羅した公開のリストは無い、でした。走査もまた、いくつあるかは教えません。与えるのは、優先順位を付けるための145件の水域ポリゴン候補です。しかも立ち入り、安全、許可が前提です。この有限のリストがあれば、現地調査を計画できます。

**JA（補足・読み上げない）**

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

**JA（訳・読み上げ可）**

このスライドは、8月31日の島への再訪についてです。それが何であって、何でないかを、はっきりさせます。これは最初のひと目です。検証ではありません。

行き先の選び方をお話しします。公開している145件のポリゴンは、候補ごとに座標と面積を持っています。短いリストを作るのは簡単です。ただ、道筋を決めるのは面積の順位ではありません。今も採石が続く島では、安全と許可、そしてそもそも歩いて行けるかどうかが、どの池がいちばん大きいかよりも大事です。ですからこれらの地点は、精度を測るために設計された標本ではありません。訪問を試みる対象として選んだ候補です。

この枠に入っている写真は、候補を示すためのもので、精度を検証するためのものではありません。走査が指した場所を地上から見るとどう見えるか、それだけを示しています。ここにある候補を、歴史記録上の特定の丁場として同定してはいません。いくつ当たって、いくつ外れたかという集計もしていません。このスライドに精度の数字はありませんし、一日の写真からそれが出ることもありません。

こういう訪問が変えるのは、数字ではありません。衛星が指したから、その場所へ歩いて行く。これは、歩き回っていて偶然池に行き当たるのとは、まったく違う働き方です。3月は、島が見せるものを私が見ていました。今回はリストが先にあります。そのリストは、オープンデータとオープンソースのコードから出てきます。この仕事のうち、他の島へ持って行けるのは、その部分です。

**JA（補足・読み上げない）**

- **[UPDATE AFTER 2026-08-31]** 再訪の実施後にこのスライドを見直す。英語本文と日本語原稿は再訪前に書いたため、まだ起きていない出来事・情景・感想を語らず、候補の選び方と写真が示す範囲、そして留保だけで構成してある。写真が確定したら、実際に写っているものに合わせて両方の原稿を書き直す。
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

**JA（訳・読み上げ可）**

先へ進む前に、この結果の限界をはっきり述べます。

まず10メートルの解像度です。幅が10メートルより狭い池は信頼できません。あの島には、細く水の溜まった切り跡があります。次に、ゼロを下回る閾値です。これは暗い岩肌や濃い影を取り込みます。小さな池を残すために払った代償です。そして、適合率も再現率もありません。その数字を出す現地検証をしていないからです。

私が検出しているのは水域であって、丁場ではありません。自然の池も水です。農業用のため池も水です。貯水施設も水です。海岸線の近くでは、ポリゴンに海が入ることもあります。私はそれらを分けていません。

もうひとつ、さきほど触れたことです。植生は本当の問題になると思っていました。この実行でマスクが変えたのは9画素だけで、この結果に足したものはほとんどありませんでした。

次の一手は単純ですが、欠かせません。候補を歩くこと。海岸線が入り込まないように陸域のマスクを足すこと。細い池には、もっと解像度の高い画像を試すこと。どれも新しい手法を必要としません。必要なのは、誰かが行って見ることです。

**JA（補足・読み上げない）**

- 限界は弁明せず短く言い切る。ここで補足を足すほど弱く聞こえる。
- 冒頭は「次に進む前に限界を明示する」という前置きで入る。11枚版（再訪スライドなしで規模対比の直後）でもそのまま成立する言い方にしてある。
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

**JA（訳・読み上げ可）**

次の一手のために、145件のポリゴンはもうオープンデータです。GeoJSON、EPSG 4326 で公開しています。その気になれば、今日の午後 QGIS で開けます。

公開しているのは何でしょうか。検出したポリゴンです。パイプラインは現地調査や遺産記録のためにラスタも書き出しますが、これは出力形式で公開物ではありません。

使っているのはオープンソースの Python ライブラリです。Rasterio、NumPy、Shapely などです。ライセンス費用はかからず、画像を買う必要もありません。

同じ手順は瀬戸内の他の採石の島にも広げられます。そういう島はいくつもあります。試すときの注意がひとつあります。私の閾値をそのまま持ち込まないでください。あれはこの島、この季節、この水のヒストグラムから出ました。ご自分で導いてください。

画像は2025年の Copernicus Sentinel データを加工したもので、成果は CC BY 4.0 です。

**JA（補足・読み上げない）**

- 公開物（GeoJSON）とパイプライン出力（GeoTIFF）を混同しない。この区別を英語で必ず言う。
- ライブラリ名の6連続は口頭では潰れるため、発話は3つに絞る。残りはフッターの投影で足りる。
- `EPSG 4326` に触れる場合は `E-P-S-G four three two six` と1文字ずつ読む。
- 帰属表記（Copernicus・CC BY 4.0）はここと主結果のスライドで口頭にも載せる。

---

### Slide 12 — Check them on the ground, then put them on the map

**EN (spoken)**

So here is the loop I would like to leave you with.

A satellite scan turns an unknown into a finite candidate list. A field visit turns a candidate into something you have seen with your own eyes. And OpenStreetMap is where what you confirmed stops being my private file and becomes a public map that anyone can use.

I plan to contribute the ponds I can confirm. I want to be clear that this is a plan. I have not done it yet, and I will only add the ones I have actually stood in front of.

In March, the mapping party added features observed on the ground. The scan suggests where to look next. That is the whole idea.

Thank you. I am happy to take questions.

**JA（訳・読み上げ可）**

最後に、ひとつの循環をお伝えしたいです。

衛星の走査は、分からないものを有限の候補リストに変えます。現地の訪問は、候補を自分の目で見たものに変えます。そして OpenStreetMap は、確かめたものが私の手元のファイルであることをやめて、誰でも使える公共の地図になる場所です。

私は、確認できた池を提供する計画です。これは計画だという点を、はっきりさせておきます。まだ実行していません。そして追加するのは、実際に自分がその前に立ったものだけです。

3月のマッピングパーティは、地上で観察した地物を追加しました。走査は、次にどこを見るべきかを示します。それが、この考え方の全体です。

ありがとうございました。質問をお受けします。

**JA（補足・読み上げない）**

- 「まだ地図にない」という欠落の指摘で終わらせない。前向きなループの提案で閉じる。
- OSMへの還元を既に行ったと述べない。この留保を英語で必ず言う。
