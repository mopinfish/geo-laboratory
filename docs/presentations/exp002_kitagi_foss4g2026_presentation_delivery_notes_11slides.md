# FOSS4G 2026 Hiroshima 北木島 口頭発表 配布用スピーカーノート（最終11枚版）

指定された最終PPTX（11枚版）のノートペインと同期したレビュー済み原稿です。英語を発話し、日本語は練習・確認用に使います。各スライドは英日9組で、S10のプレースホルダー画像は後日差し替えます。

## Slide 1

Good afternoon, everyone.
みなさん、こんにちは。

Please look at this wall.
この壁を見てください。

It is not a natural wall.
これは自然にできた壁ではありません。

People cut granite on this island for about four hundred years.
人々はこの島で約400年間、花崗岩を切り出しました。

At this scale, we can see the history from the ground.
この縮尺では、地上から歴史を見ることができます。

They changed the shape of the land little by little.
人々は少しずつ、土地の形を変えていきました。

After the work stopped, water collected at the bottom.
採石が止まったあと、底に水が溜まりました。

This is a photo from the island, not a map or a result.
これは島で撮った写真で、地図や分析結果ではありません。

Today, I will show this same island at three different scales, from the ground to space.
今日は、この同じ島を地上から宇宙まで、三つの違う縮尺でお見せします。

## Slide 2

Kitagi Island is in Kasaoka City, Okayama Prefecture.
北木島は岡山県笠岡市にあります。

It is in the Seto Inland Sea.
瀬戸内海にある島です。

It is the largest island in the Kasaoka Islands.
笠岡諸島の中で一番大きな島です。

People began to quarry granite there in the early seventeenth century.
17世紀の初めから、ここで花崗岩が切り出されました。

At the peak, there were 127 active quarry sites on the island.
最盛期には、島に127か所の採石場がありました。

About 12,000 people lived there at that time.
そのころは約1万2千人が暮らしていました。

This is a living island, not only an old industrial site.
ここは古い産業遺産だけでなく、今も人が暮らす島です。

Today, two quarries still work, and about 600 to 700 people live there.
現在も二つの丁場が稼働し、約600〜700人が暮らしています。

Some old pits filled with rainwater and groundwater, but I found no complete island-wide pond list.
古い採石跡の一部には雨水や地下水が溜まりましたが、島全体の池の完全なリストは見つかりませんでした。

## Slide 3

My story began in March 2026.
私の調査は2026年3月に始まりました。

I joined a two-day drone mapping event.
2日間のドローン・マッピングに参加しました。

On foot, I saw walls cut straight into the granite.
地上では、花崗岩をまっすぐ切ってできた壁を見ました。

The walls looked very different from natural rock.
その壁は、自然の岩とは大きく違って見えました。

I also saw dark green water in the old pits.
古い採石跡には、濃い緑色の水も見えました。

Some public records report depths from a few metres to about twenty metres.
公開記録には、水深が数メートルから約20メートルと書かれています。

I did not measure the depth myself.
私は水深を自分で測ったわけではありません。

The visit showed me why a map must start with real places.
この訪問で、地図は実際の場所から始めるべきだと分かりました。

In two days, I visited only five or six sites, so I needed a wider view.
2日間で訪ねられたのは5〜6か所だけだったので、もっと広い視点が必要でした。

## Slide 4

On the second day, we flew a drone from the stage on the water.
2日目に、水上ステージからドローンを飛ばしました。

The island looked very different from the air.
空から見ると、島は大きく違って見えました。

The quarries looked like grey rectangles in a green forest.
採石跡は、緑の森の中の灰色の四角形に見えました。

The straight edges showed where people had cut the granite.
まっすぐな縁から、人々が花崗岩を切った場所が分かりました。

A thin granite wall stood between two large pits.
大きな二つの採石跡の間に、細い花崗岩の壁が残っていました。

This wall marked the boundary between two companies’ sites.
この壁は、二つの会社の採石地の境界を示していました。

A line on an old document became a real landform.
古い書類の線が、実際の地形になっていたのです。

The drone gave us a wider view, but it still covered only part of the island.
ドローンは広い視点をくれましたが、それでも島の一部しか見ていません。

We also added some features seen on the ground to OpenStreetMap, but only in the places we visited.
地上で見た地物の一部はOpenStreetMapにも追加しましたが、訪ねた場所だけです。

## Slide 5

On the train home, I thought about the whole island.
帰りの電車で、島全体のことを考えました。

Five or six sites were only a small part of the island.
5〜6か所は、島のほんの一部です。

One freely available satellite image could cover the whole island.
無料で利用できる衛星画像なら、1枚で島全体を覆えます。

This made satellite data a natural next step for the project.
そこで、次の段階として衛星データを使うことにしました。

I used Sentinel-2 data from 2 August 2025.
2025年8月2日のSentinel-2データを使いました。

The image had very little cloud, and the grid was ten metres.
画像の雲はとても少なく、格子の大きさは10メートルでした。

NDWI and MNDWI helped find pixels that may contain water.
NDWIとMNDWIで、水を含むかもしれない画素を探しました。

NDVI helped remove many green plants from the result.
NDVIで、結果から多くの緑の植物を除きました。

I kept connected water areas of at least one hundred square metres, so the result became a useful list.
つながった水域のうち100平方メートル以上のものを残し、使いやすいリストにしました。

## Slide 6

The summer scan found 145 water polygons on the island.
夏の走査では、島に145件の水域ポリゴンが見つかりました。

Each polygon was at least one hundred square metres.
それぞれのポリゴンは、100平方メートル以上です。

The number tells us how many areas were detected, not how many quarries remain.
この数は検出された水域の数であり、残る採石跡の数ではありません。

The spring scan reported 113 polygons.
春の走査では、113件と報告されました。

The two numbers are different, but we do not know the reason yet.
二つの数字は違いますが、理由はまだ分かっていません。

The spring processing settings were not saved in full.
春の処理設定は、すべて保存されていませんでした。

So I do not call this a proven seasonal change.
そのため、季節による変化だとは断定していません。

The detected polygons were also concentrated in some areas with many old quarry records.
検出されたポリゴンは、古い採石記録が多い地域にも集中していました。

These are detected water areas, not field-confirmed quarry ponds, so the number is a starting point for fieldwork.
これは検出された水域で、現地確認済みの丁場池ではないため、この数は現地調査の出発点です。

## Slide 7

These three scales show different parts of the island.
この三つの縮尺は、島の違う部分を見せてくれます。

On foot, I could see the cut face and the water closely.
地上では、切った岩肌と水を近くで見られます。

I could also understand the space and depth around me.
周囲の空間や深さも実感できました。

But I could see only one place at a time.
しかし、一度に見られるのは一つの場所だけです。

From the air, I could see quarry boundaries.
空からは、採石跡の境界が見えます。

The thin granite wall was a good example.
細い花崗岩の壁が、そのよい例です。

From orbit, one image showed 145 candidates across the island.
軌道上からは、1枚の画像で島全体の145件の候補が見えました。

The scales work together like three different windows onto the same place.
三つの縮尺は、同じ場所を見る三つの窓のように役立ちます。

No single scale is best; we need all three to understand the full picture.
どれか一つの縮尺が最善というわけではありません。全体を理解するには三つすべてが必要です。

## Slide 8

I visited five or six sites on the ground.
私は地上で5〜6か所を訪ねました。

The satellite scan produced 145 water-polygon candidates.
衛星走査では、145件の水域ポリゴン候補が出ました。

This difference shows why a whole-island scan is useful.
この違いから、島全体の走査が役立つことが分かります。

It helps us see places that we cannot reach in one short visit.
短い訪問では行けない場所も、見ることができます。

This list helps us plan work, but it does not replace local knowledge.
このリストは作業計画に役立ちますが、地域の知識に代わるものではありません。

I cannot say that my five or six sites match five or six candidates.
私が訪ねた5〜6か所が、5〜6件の候補と一致するとは言えません。

I did not match each visit with a polygon.
訪問場所とポリゴンを一つずつ対応させていないからです。

All seven named quarry features in the area overlapped a detected polygon, but this is only a reference.
対象範囲内の名前付き採石場地物7件は検出ポリゴンと重なりましたが、これは参考情報です。

The 145 candidates give us a finite list for safer and more focused field visits.
145件の候補は、より安全で集中した現地調査のための有限のリストになります。

## Slide 9

Now, I want to explain what this scan cannot tell us.
ここで、この走査では分からないことを説明します。

The image resolution is ten metres.
画像の解像度は10メートルです。

Ponds narrower than about ten metres are difficult to detect reliably.
幅が約10メートル未満の池は、信頼性をもって検出するのが難しくなります。

One pixel may contain water, granite, and shadow together.
一つの画素に、水、花崗岩、影が一緒に入ることがあります。

Dark rock and shadow may also look like water.
暗い岩や影も、水のように見えることがあります。

A careful answer needs both satellite data and field checks.
慎重に判断するには、衛星データと現地確認の両方が必要です。

The scan finds water, not old quarries themselves.
走査が見つけるのは水であり、古い採石跡そのものではありません。

Natural ponds and reservoirs may enter the results, and coastal water may also enter them.
自然の池やため池が結果に入ることがあり、海岸付近の水域が入る可能性もあります。

I have not measured precision or recall, so we need field visits and clearer images next.
適合率や再現率は測っていないため、次は現地訪問とより鮮明な画像が必要です。

## Slide 10

On 31 August, I visited the island again.
8月31日に、もう一度島を訪れました。

This visit was a first look, not an accuracy test.
今回の訪問は最初の確認であり、精度検証ではありません。

I used the candidate locations from the published GeoJSON.
公開したGeoJSONの候補位置を使いました。

I first checked if the places were safe to approach.
まず、その場所に安全に近づけるかを確認しました。

I also needed permission and a path that was easy to walk.
許可と、歩きやすい道も必要でした。

The return visit showed a practical way to move from data to action.
再訪によって、データを行動につなげる実際の方法が見えてきました。

Safety and permission were more important than area ranking.
面積の順位よりも、安全と許可を大切にしました。

The photos show places pointed out by the scan.
写真は、走査が示した場所を写しています。

They do not prove that every detection is correct, but they show how the list can guide a visit.
すべての検出が正しいことを証明するものではありませんが、リストが訪問を案内する様子を示しています。

## Slide 11

The main idea today is simple.
今日の主な考え方はシンプルです。

A satellite scan gives us a list of places to check.
衛星走査は、確認する場所のリストを作ります。

A field visit lets us see each place with our own eyes.
現地訪問では、それぞれの場所を自分の目で見られます。

We can then compare the image with the real ground.
そのあとで、画像と実際の地面を比べられます。

We should add only the water areas that we confirm in the field.
現地で確認できた水域だけを追加するべきです。

OpenStreetMap can share that information with everyone.
OpenStreetMapなら、その情報をみんなと共有できます。

Open data is useful when its limits are also explained clearly.
オープンデータは、その限界も分かりやすく説明すると役立ちます。

In March, we mapped what we saw on the ground.
3月には、地上で見たものを地図にしました。

Now, the satellite scan tells us where to look next, and this connects local knowledge with open data. Thank you.
今度は衛星走査が次に見る場所を教えてくれます。これで地域の知識とオープンデータがつながります。ありがとうございました。
