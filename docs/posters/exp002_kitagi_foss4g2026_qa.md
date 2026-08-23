# FOSS4G Hiroshima 2026 ポスター 想定問答集（英日併記）

対象ポスター: `exp002_kitagi_quarry_foss4g2026_poster.pdf` — *Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools* / Noboru Otsuka (Geolonia Inc.)

口頭説明スクリプトは `exp002_kitagi_foss4g2026_talk_script.md`。コアタイム中はスマートフォンで本ファイルを開ける状態にしておく。

---

## 0. 回答の原則

1. **裏付けのない質問には「未検証です」と答える。** 精度指標、個別の丁場同定、経年変化はいずれも未実施。推測を数値で語らない。
2. **数値の階層を守る。** Tier 1 は**ポスターに掲載されている値すべて**（主要値: 113 / 145 / 127 / 9 px / 100 m² / 10 m / 20 m / 2025-03-23 / 2025-08-02 / 雲量 0.0% / 0.7% / −0.2 / −0.1 / 0.3。網羅列挙ではない）で、自由に使う。Tier 2 はポスターに無く報告書のみに基づく補足値で、同一行に `[report]` / `[報告書]` を付し、口頭で出す際は「ポスターには載せていない報告書の値」と添える。Tier 3（報告書の推定）は *may / possibly* のヘッジを外さない。
3. **「検出水域」と「現地確認済みの丁場池」を混ぜない。** 英語では *detected water polygons* / *candidates* を使う。丁場池を「確認済み」と述べてよいのは、`not (individually) field-confirmed …` のように対象句を直接否定する構文のときだけ。
4. **145 と 127 の関係は規模比較。** 1対1対応と読める言い方をしない。

---

## 1. 手法（指数の選択）

### Q1-1. Why use both NDWI and MNDWI instead of one index?
- **JP:** なぜNDWIとMNDWIを併用するのですか。単独では不十分ですか。
- **A (EN):** They fail differently. NDWI uses green and near-infrared and is the standard for open water; MNDWI uses green and short-wave infrared and separates water from bare rock much better, which matters on a granite island. I take the union so a pond only needs to pass one of them.
- **A (JP):** 失敗の仕方が違うからです。NDWIは緑と近赤外を使う開放水面の標準指標、MNDWIは緑と短波赤外を使い、水域と裸地・岩肌の分離に優れます。花崗岩の島ではこれが重要です。和集合を取ることで、どちらか一方を通れば検出される設計にしています。
- 根拠: 報告書 3.3、5.1（仮説1）／McFeeters 1996、Xu 2006、Du et al. 2016

### Q1-2. MNDWI needs SWIR, which is 20 m. Doesn't that break your 10 m claim?
- **JP:** MNDWIに使うSWIRは20 mですが、10 mという主張と矛盾しませんか。
- **A (EN):** Fair point, and the poster states it: B11 is natively 20 metres and I resample it bilinearly to the 10-metre grid. So the analysis grid is 10 metres, but the MNDWI information content is 20-metre. NDWI and NDVI use only native 10-metre bands.
- **A (JP):** 正当な指摘で、ポスターにも明記しています。B11はネイティブ20 mで、バイリニア補間により10 mグリッドへリサンプリングしています。解析グリッドは10 mですが、MNDWIの情報量は20 m相当です。NDWIとNDVIはネイティブ10 mバンドのみを使っています。
- 根拠: 報告書 3.2（バンド表）、ポスター §3・§4・F4キャプション

### Q1-3. Why not supervised classification, or SAR?
- **JP:** 教師あり分類やSARを使わないのはなぜですか。
- **A (EN):** Two reasons: there is no labelled ground truth for this island yet, and I wanted a workflow anyone can rerun with three formulas and no training data. SAR would help with shadowed pits, but I have not tested it — it's a reasonable next experiment.
- **A (JP):** 理由は2つです。この島にはまだ教師データがないこと、そして訓練データ不要で3つの式だけで誰でも再実行できるワークフローにしたかったことです。SARは影に落ちた採石跡に有効だと思いますが、未検証です。次の実験候補としては妥当だと考えています。
- 根拠: 報告書 2.3（本研究の位置づけ）、6.3。SARは未実施のため推測であることを明示する

### Q1-4. Why does the NDVI mask matter if it only removed 9 pixels?
- **JP:** 9ピクセルしか除外していないNDVIマスクに意味はあるのですか。
- **A (EN):** Honestly, not in this scene — that was my third hypothesis and it was rejected. The vegetation mask itself covered a large area `[report: 72,636 px]`, but it barely overlapped the water candidates, so only 9 pixels changed. I keep it as a low-cost safeguard: it will matter when the workflow moves to greener islands.
- **A (JP):** 正直に言えば、このシーンでは意味がありませんでした。3番目の仮説として立て、棄却されました。植生マスク自体は広い面積を覆っています `[報告書: 72,636 px]` が、水域候補との重複がほとんどなく、変化したのは9ピクセルだけでした。低コストな安全策として残しています。より緑の多い島へ展開するときには効くはずです。
- 根拠: 報告書 4.2（表4-2）、5.1（仮説3は棄却）

---

## 2. 閾値

### Q2-1. Why are your thresholds negative? The textbook value for NDWI is zero.
- **JP:** なぜ閾値が負の値なのですか。NDWIの教科書的な閾値は0のはずです。
- **A (EN):** Because of spectral mixing at 10 metres. These ponds are narrow and walled in, so a pixel is part water, part granite, part shadow, and the index value gets pulled down well below zero. A threshold of zero simply misses them. I set NDWI above −0.2 and MNDWI above −0.1.
- **A (JP):** 10 m解像度でのスペクトル混合のためです。対象の池は細く岩壁に囲まれているので、1ピクセルに水・花崗岩・影が混ざり、指数値が0よりかなり下に引き下げられます。閾値0では取りこぼします。そのためNDWI > −0.2、MNDWI > −0.1に設定しました。
- 根拠: 報告書 3.4、5.1（仮説1）、ポスター §4

### Q2-2. How did you choose −0.2, −0.1 and 0.3? Are they tuned?
- **JP:** −0.2、−0.1、0.3はどう決めたのですか。チューニングしたのですか。
- **A (EN):** For NDWI and NDVI, from the index histograms rather than an optimisation: NDWI has a land peak near −0.5 and a sea peak around 0.05 to 0.15, so −0.2 sits in the valley between them, and NDVI 0.3 sits in the valley between the bare-surface peak near zero and the vegetation sub-peak at 0.5 to 0.7 `[report]`. For MNDWI, −0.1 has no independent documented basis — it was set in the same spirit of allowing spectrally mixed pixels through. None of the three has been optimised, sensitivity-tested or field-validated.
- **A (JP):** NDWIとNDVIについては、最適化ではなく指数のヒストグラムから決めています。NDWIは陸域ピークが−0.5付近、海域ピークが0.05〜0.15付近にあり、−0.2はその谷に位置します。NDVIの0.3は、0付近の裸地ピークと0.5〜0.7の植生サブピークの谷にあります `[報告書]`。MNDWIの−0.1については独立した根拠を文書化していません。スペクトル混合したピクセルを通す、という同じ考え方で設定した値です。3つとも最適化・感度分析・現地検証はしていません。
- 根拠: 報告書 4.2（図4-2 ヒストグラム）、5.4 第3項

### Q2-3. Did you run a sensitivity analysis?
- **JP:** 閾値の感度分析はしましたか。
- **A (EN):** Not systematically, and I won't pretend otherwise. I can tell you the direction: relaxing the thresholds adds coastal and shadow polygons, tightening them drops the small ponds first. Quantifying that trade-off needs the field validation set.
- **A (JP):** 体系的には行っていません。方向性は言えます。閾値を緩めると海岸線や影のポリゴンが増え、締めると小規模な池から落ちていきます。このトレードオフの定量化には現地検証データが必要です。
- 根拠: 報告書 5.4 第3項、6.3 第2項。感度分析は未実施

---

## 3. 季節差（113 vs 145）

### Q3-1. Why does summer find more than spring? Which one should I trust?
- **JP:** なぜ夏季の方が多いのですか。どちらが信頼できるのですか。
- **A (EN):** Neither replaces the other — the seasonal difference is a difference in detection characteristics, not a ranking. Spring has a much wider index range and is better on the large ponds; summer returns more polygons and is better on the small ones. I treat the two dates as two different observations, not interchangeable ones.
- **A (JP):** どちらか一方が上位ということではありません。季節差は検出特性の違いです。春季は指数の値域が広く大型水域に強く、夏季はポリゴン総数が多く小規模水域に強い。2時期は「入れ替え可能な観測」ではなく「別の観測」として扱っています。
- 根拠: 報告書 4.4（表4-4）、ポスター §6 最終項

### Q3-2. Is the difference real water-level change, or just detection difference?
- **JP:** 差は実際の水位変動ですか、それとも検出特性の違いですか。
- **A (EN):** I can't separate them with two scenes, so I don't claim water-level change. What I can show is that the summer index range was much narrower — the summer NDWI maximum was 0.210 against 1.000 in spring `[report]`. That points to sensor and atmospheric conditions, not only to the ponds.
- **A (JP):** 2シーンでは分離できないので、水位変動だとは主張しません。示せるのは、夏季の指数値域が大幅に狭かったことです。夏季のNDWI最大値は0.210、春季は1.000でした `[報告書]`。これは池そのものだけでなく、センサ・大気条件の影響を示しています。
- 根拠: 報告書 4.4、5.2

### Q3-3. Why was the summer index range so much narrower?
- **JP:** 夏季の指数値域が狭かった理由は何ですか。
- **A (EN):** Three plausible causes, and I have not separated them: more atmospheric water vapour reducing near-infrared transmission, warmer and more turbid seawater lowering the sea's NDWI, and a higher solar elevation angle changing surface reflection. It's a hypothesis list, not a finding.
- **A (JP):** 考えられる要因は3つあり、分離できていません。大気の水蒸気量増加による近赤外の透過率低下、海水温上昇と懸濁物質による海域NDWIの低下、太陽高度角の違いによる水面反射の変化です。これは仮説のリストであって、結論ではありません。
- 根拠: 報告書 5.2

### Q3-4. Why these two dates in 2025?
- **JP:** なぜ2025年のこの2日を選んだのですか。
- **A (EN):** The study plan set the window at 2023 through 2025 with a 10 percent cloud ceiling and a preference for low-cloud scenes; the reported scenes have 0.0 percent cloud in spring and 0.7 percent in summer. For the summer scene the committed notebook reproduces that: it sorts candidates by cloud cover and takes the least-cloudy summer-month scene. For spring, the exact historical selection procedure was not preserved — the same gap as the 113 figure — so I can't tell you more than the plan and the reported cloud cover.
- **A (JP):** 計画では検索期間を2023年〜2025年、雲量上限10%とし、雲量の少ないシーンを優先することにしています。報告しているシーンの雲量は春季0.0%、夏季0.7%です。夏季についてはコミット済みのノートブックで再現できます。候補を雲量昇順に並べ、夏季月のうち最も雲量の少ないシーンを取る実装です。春季については当時の選定手順が保存されていません（113の件と同じ欠落です）ので、計画の基準と報告した雲量以上のことは言えません。
- 根拠: `docs/plans/exp002_kitagi_quarry_water_detection.md`「画像選択基準」、報告書 3.2、報告書 4.1 追記（春季の再現性）、`notebooks/exp002_kitagi_quarry_water_detection.ipynb`（雲量昇順ソート＋夏季月の先頭を選択）

---

## 4. 偽陽性・水域の性質

### Q4-1. How many of the 145 are actually natural ponds or irrigation reservoirs?
- **JP:** 145件のうち、自然の池沼や農業用ため池はどれくらい含まれますか。
- **A (EN):** Unknown — that's exactly the limitation on the poster. Natural ponds, reservoirs, shadows and dark rock can all pass a negative threshold. Until we check them in the field, every polygon is a candidate.
- **A (JP):** 不明です。これはポスターに書いた限界そのものです。自然の池沼、ため池、影、暗い岩肌はいずれも負の閾値を通り得ます。現地で確認するまで、すべてのポリゴンは候補です。
- 根拠: 報告書 5.4 第5項、ポスター §5 の注意文言

### Q4-2. What about shadows from the granite walls? Those pits are deep.
- **JP:** 花崗岩の岩壁による影はどうですか。採石跡は深いですよね。
- **A (EN):** Shadow is the failure mode I worry about most. It cuts both ways: a shadowed water surface can drop below the threshold and be missed, and dry shadowed rock can look water-like and be a false positive. I haven't quantified either, and no illumination or terrain correction is applied.
- **A (JP):** 影は最も懸念している失敗モードです。両方向に効きます。影に落ちた水面は閾値を下回って見落とされ、乾いた影の岩肌は水域的に見えて誤検出になります。どちらも定量化していません。照度補正・地形補正も適用していません。
- 根拠: 報告書 5.4 第3項。影の定量評価は未実施

### Q4-3. Did you separate the sea from the island's water bodies?
- **JP:** 海域と島内水域の分離はどうしていますか。
- **A (EN):** Only partially. I exclude the sea polygon itself, but I do not apply a strict coastline mask, so polygons near the shore may still contain seawater. Adding a proper land mask is the first item on my to-do list.
- **A (JP):** 部分的にしか分離できていません。海域のポリゴン自体は除外していますが、厳密な海岸線マスクは適用していないため、海岸線付近のポリゴンには海水が含まれる可能性があります。陸域マスクの導入が今後の課題の第1項です。
- 根拠: 報告書 5.4 第2項、6.3 第1項

### Q4-4. How small a pond can you actually see?
- **JP:** 実際にどのくらい小さい池まで見えるのですか。
- **A (EN):** The reporting floor is 100 square metres — about one Sentinel-2 pixel — and polygons below that are excluded, so smaller ponds are simply not in the inventory. Above that floor, a pond narrower than roughly 10 metres is difficult and unreliable regardless of its area, because no pixel is purely water. The smallest polygon in the published set is just over 100 square metres.
- **A (JP):** 報告の下限は100 m²で、Sentinel-2の約1ピクセルに相当します。これ未満のポリゴンは除外しているので、それより小さい池はインベントリに入っていません。下限より大きくても、幅が10 m程度未満の池は面積にかかわらず検出が難しく信頼できません。純粋に水だけのピクセルが存在しないためです。公開しているデータの最小ポリゴンは100 m²を少し超える程度です。
- 根拠: 報告書 5.4 第1項、ポスター §3・10 m カウント

### Q4-5. How exactly do you decide a polygon is "intra-island"?
- **JP:** 「島内」の判定は具体的にどうしているのですか。
- **A (EN):** Two mechanical rules: the polygon's area must be under 10 hectares, which drops the sea itself, and its centroid must fall inside the island's bounding box. That's it — no coastline geometry is involved, which is exactly why coastal polygons remain a known weakness.
- **A (JP):** 機械的な2つのルールです。ポリゴンの面積が10 ha未満であること（これで海域そのものが落ちます）、そして重心が島のバウンディングボックス内にあること。それだけです。海岸線のジオメトリは使っていません。だからこそ海岸線付近のポリゴンが既知の弱点として残っています。
- 根拠: `scripts/generate_exp002_poster_figures.py`（`SEA_AREA_THRESHOLD_M2 = 100_000`、`KITAGI_BBOX` による重心判定）、報告書 5.4 第2項

---

## 5. 現地検証

### Q5-1. What's your accuracy? Precision and recall?
- **JP:** 精度はどれくらいですか。適合率・再現率は。
- **A (EN):** I don't have them. There is no validated reference set for this island, so computing precision and recall would be fabrication. That is the single biggest gap in this work and the reason the poster says "candidates".
- **A (JP):** ありません。この島には検証済みの参照データセットが存在しないため、適合率・再現率を出すと捏造になります。これが本研究の最大の欠落で、ポスターが「候補」と書いている理由です。
- 根拠: 報告書 5.4 第5項、6.3 第2項

### Q5-2. How will you validate? What's the plan?
- **JP:** どう検証する計画ですか。
- **A (EN):** Take the candidate layer to the island as GeoJSON on a mobile GIS, check polygons against known quarry locations and the municipal records, then compute precision and recall against that set. The 145 polygons make that a finite, plannable job rather than an open-ended survey.
- **A (JP):** 候補レイヤをGeoJSONでモバイルGISに載せて島へ持ち込み、既知の丁場位置や自治体の記録と照合し、その集合に対して適合率・再現率を算出します。145件という有限の数になっているので、無際限の踏査ではなく計画可能な作業になります。
- 根拠: 報告書 6.3 第2項、ポスター Conclusion

### Q5-3. Can local stakeholders use this before validation?
- **JP:** 検証前でも地元にとって使えるものですか。
- **A (EN):** As a screening layer, yes — it tells you where to look first, and safety management around unfenced flooded pits is a real local concern. It is not evidence for any individual site, and I'd say that clearly to any municipality using it.
- **A (JP):** スクリーニングのレイヤとしては使えます。どこを先に見るべきかが分かりますし、柵のない水没採石跡の安全管理は地元の実際の課題です。ただし個別地点の根拠にはなりません。自治体が使う場合はその点を明確に伝えます。
- 根拠: 報告書 1.1（保全・観光・安全管理）、6.2

---

## 6. 春季結果の再現性

### Q6-1. Why does the poster say the spring configuration is "not preserved"?
- **JP:** 春季の設定が「保存されていない」とはどういう意味ですか。
- **A (EN):** 113 is the figure reported from our run in March 2026, and that run's exact configuration was not preserved in the repository. Re-running the current pipeline on the same scene gives 180 intra-island polygons `[report]`. The index statistics match the original, which tells us the input scene is the same, but we have not isolated where the difference comes from — the historical code state, post-processing and environment are equally unrecorded. So: 113 is the reported figure, 180 is the current recomputation, and I'd rather state both than quietly swap the number.
- **A (JP):** 113は2026年3月の実行で報告した値で、その実行の設定はリポジトリに保存されていませんでした。同一シーンに現行パイプラインを適用すると島内180ポリゴンになります `[報告書]`。指数統計は当初と一致しているので入力シーンは同じですが、差がどこから来ているかは特定できていません。当時のコードの状態・後処理・実行環境も同様に記録されていないためです。113は報告値、180は現行の再計算値であり、黙って差し替えるより両方を述べる方がよいと考えました。
- 根拠: 報告書 4.1 追記（2026-08-14）、5.4 第6項、ポスター §5 の注記

### Q6-2. Then why keep 113 on the poster at all?
- **JP:** ならばなぜ113をポスターに残しているのですか。
- **A (EN):** Because 113 is the number in the report that this poster presents, and replacing it with an unreviewed recomputation would be a different claim. The poster states the reproducibility limit directly under the number, so the caveat travels with the figure.
- **A (JP):** 113はこのポスターが提示している報告書の値であり、レビューを経ていない再計算値に差し替えるのは別の主張になってしまうからです。数値の直下に再現性の限界を明示しているので、注記は数値と一緒に読まれます。
- 根拠: ポスター §5 注記、内容契約（Tier 1 のロック値）

### Q6-3. Is the summer result reproducible?
- **JP:** 夏季の結果は再現できるのですか。
- **A (EN):** Yes, fully. The 145 figure and the 9-pixel vegetation exclusion both reproduce from the current repository, and the poster figures are regenerated by a script that verifies those values before drawing.
- **A (JP):** 完全に再現できます。145件と植生マスクによる9ピクセルの除外は、いずれも現行リポジトリから再現されます。ポスターの図版は、描画前にこれらの値を検証するスクリプトで生成しています。
- 根拠: `scripts/generate_exp002_poster_figures.py`（確定値検証）、報告書 4.1 追記

---

## 7. 歴史的丁場との対応（127）

### Q7-1. You detected 145 and there were 127 quarries. Is that a match?
- **JP:** 145件検出で丁場は127か所。対応しているということですか。
- **A (EN):** It's a comparison of scale, not a one-to-one match. I have not linked a single polygon to a specific quarry. The meaningful part is the spatial pattern: detections cluster in the north, south-east, centre and west, and the north was the industrial core historically.
- **A (JP):** 規模の比較であって、1対1の対応ではありません。個別のポリゴンを特定の丁場に結びつけてはいません。意味があるのは空間パターンです。検出は北部・南東部・中央部・西部に集中し、歴史的に採石の中心は北側でした。
- 根拠: 報告書 5.1（仮説2は部分的支持）、5.3、ポスター §6 第1項

### Q7-2. Any specific pond you can name?
- **JP:** 特定できている池はありますか。
- **A (EN):** One candidate, and I'll keep the hedge: the large water body detected in the south-east may correspond to the former Imaoka quarry known locally as "Kitagi no Keirin". That is a plausible correspondence from local records, not a verified identification.
- **A (JP):** 一つ候補はありますが、留保は付けたままにします。南東部で検出された大型水域は、旧今岡石材の丁場跡「北木の桂林」に相当する可能性があります。地域の記録から見て妥当な対応ですが、検証された同定ではありません。
- 根拠: 報告書 5.3（Tier 3・ヘッジ必須）

### Q7-3. Could satellite imagery detect quarries that history forgot?
- **JP:** 記録に残っていない丁場を衛星画像で見つけられる可能性はありますか。
- **A (EN):** That's the appealing possibility, and it's untested. Any polygon that has no counterpart in the records is either an undocumented pit or a false positive, and only fieldwork can tell those apart. It's a good reason to do the field campaign.
- **A (JP):** 魅力的な可能性ですが、未検証です。記録に対応がないポリゴンは、未記録の丁場か誤検出のどちらかで、それを区別できるのは現地調査だけです。現地調査を行う十分な動機だと考えています。
- 根拠: 報告書 5.4 第5項、6.3 第2項。推測であることを明示する

---

## 8. 他地域への展開

### Q8-1. Would this work on other islands?
- **JP:** 他の島でも通用しますか。
- **A (EN):** The workflow should transfer to the other quarried islands in the Seto Inland Sea — Shiraishi and Inujima are the obvious next cases `[report]`. The thresholds are the part I would not transfer blindly; they were set from this island's histograms.
- **A (JP):** 瀬戸内海の他の採石島には展開できるはずです。白石島や犬島が次の明確な候補です `[報告書]`。無条件に持ち込めないのは閾値です。この島のヒストグラムから設定したものなので。
- 根拠: 報告書 6.3 第5項、ポスター Conclusion

### Q8-2. Would it work for mining regions outside Japan?
- **JP:** 日本以外の鉱山地域でも使えますか。
- **A (EN):** In principle — Sentinel-2 is global and the indices aren't Japan-specific. What is specific here is a granite landscape where vegetation barely interferes; in a wetter, greener setting the NDVI mask would do far more work than the 9 pixels it did here.
- **A (JP):** 原理的には可能です。Sentinel-2はグローバルで、指数も日本固有のものではありません。固有なのは、植生がほとんど干渉しない花崗岩の景観です。より湿潤で緑の多い環境では、NDVIマスクはここでの9ピクセルよりはるかに大きな役割を果たすはずです。
- 根拠: 報告書 5.1（仮説3）、6.3 第5項。国外適用は未検証

---

## 9. データ・コード・ライセンス

### Q9-1. Where's the code?
- **JP:** コードはどこにありますか。
- **A (EN):** The QR code at the bottom: github.com/mopinfish/geo-laboratory. The analysis is the notebook `notebooks/exp002_kitagi_quarry_water_detection.ipynb`, and the report with all the numbers is under `docs/reports/`.
- **A (JP):** 下のQRコードから github.com/mopinfish/geo-laboratory です。分析本体はノートブック `notebooks/exp002_kitagi_quarry_water_detection.ipynb`、数値の全ては `docs/reports/` のレポートにあります。
- 根拠: ポスター フッター

### Q9-2. Can I download the GeoJSON of the 145 polygons?
- **JP:** 145件のGeoJSONはダウンロードできますか。
- **A (EN):** Yes — it's published in the repository behind the QR code, at `docs/results/exp002/`, with a README that records the generating commit, the attribution and the cautions. It's EPSG:4326, one polygon per feature with its area in square metres. The GeoTIFF isn't published; you regenerate that from the notebook.
- **A (JP):** はい。QRコードのリポジトリの `docs/results/exp002/` に公開しています。生成コミット・帰属表示・注意書きを記録したREADMEも同じディレクトリにあります。EPSG:4326で、1ポリゴン1featureに面積（m²）が付いています。GeoTIFFは公開していないので、必要ならノートブックで再生成してください。
- 根拠: `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`（145 features、生成: `scripts/generate_exp002_poster_figures.py`）、同 `_README.md`

### Q9-3. What's the software stack and does it cost anything?
- **JP:** ソフトウェア構成は。費用はかかりますか。
- **A (EN):** No licence fee for the stack and no imagery purchase: rasterio, numpy, shapely, pystac-client, planetary-computer and folium, on Python 3.11 with uv for package management, and Sentinel-2 through the Microsoft Planetary Computer STAC API. You still pay for your own compute and bandwidth.
- **A (JP):** ソフトウェアのライセンス費用と画像の購入費はかかりません。rasterio、numpy、shapely、pystac-client、planetary-computer、folium、Python 3.11、パッケージ管理はuv、画像はMicrosoft Planetary ComputerのSTAC API経由のSentinel-2です。計算資源と通信の費用は自分持ちです。
- 根拠: 報告書 3.5、ポスター §7・フッター

### Q9-4. What license? Can I reuse the poster and the figures?
- **JP:** ライセンスは。ポスターや図版を再利用できますか。
- **A (EN):** The conference contribution is CC BY 4.0, so yes, with attribution. The imagery carries its own notice: "Contains modified Copernicus Sentinel data 2025", and the location map basemap is GSI Tiles from the Geospatial Information Authority of Japan.
- **A (JP):** 本発表はCC BY 4.0なので、出典表示のうえで再利用可能です。画像には別途の表示が必要です。"Contains modified Copernicus Sentinel data [2025]"、位置図の基図は国土地理院のGSI Tilesです。
- 根拠: ポスター フッター（Attribution and license）、内容契約

### Q9-5. Which scenes exactly? I want to reproduce it.
- **JP:** 具体的にどのシーンですか。再現したいのですが。
- **A (EN):** Spring is `S2C_MSIL2A_20250323T014711` and summer is `S2A_MSIL2A_20250802T015121`, both tile T53SLU, processed in EPSG:32653 `[report]`. The bounding box and all constants are in the notebook.
- **A (JP):** 春季が `S2C_MSIL2A_20250323T014711`、夏季が `S2A_MSIL2A_20250802T015121`、いずれもタイルT53SLU、処理はEPSG:32653です `[報告書]`。バウンディングボックスと各定数はノートブックにあります。
- 根拠: 報告書 3.1、3.2

### Q9-6. How long does it take to run? What hardware?
- **JP:** 処理時間はどれくらいですか。必要なマシンスペックは。
- **A (EN):** I haven't measured it properly, so I won't quote a number. Practically it's a single Sentinel-2 scene clipped to one small island, so it runs on a laptop — the download dominates, not the computation. If you need real figures I can measure and send them.
- **A (JP):** きちんと計測していないので数値は出しません。実感としては、1シーンを小さな島の範囲に切り出すだけなのでノートPCで動きます。支配的なのは計算ではなくダウンロードです。実測値が必要であれば、計測してお送りします。
- 根拠: 未計測（定型フレーズで回答する項目）

---

## 10. 想定外の質問への構え

| 状況 | 対応 |
|---|---|
| 数値を聞かれたが手元の確定値にない | **EN:** “I don't have that measured — answering would be overclaiming. It's on the field-campaign list.” ／ **JP:** 「計測していないので、答えると過大主張になります。現地調査の項目に入れています。」 |
| 手法上の弱点を指摘された（正しい指摘） | 認めて、限界の記述を指差す。**EN:** “You're right, and that's limitation number two on the poster.” |
| 日本語で専門的に議論したい相手 | 日本語で応じる。ポスターは英語のままでよい。数値の階層ルールは日本語でも同じ |
| 個別の丁場を断定させようとする質問 | **EN:** “I can't confirm any individual pond — that's exactly what's not validated yet.” |
| 連絡先交換 | リポジトリURLと発表者名（Noboru Otsuka / Geolonia Inc.）を渡す。データ送付を約束した場合はその場でメモを取る |

---

## 11. 出典一覧

| 区分 | 参照 |
|---|---|
| ポスター掲載文言・Tier 1 数値 | `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md`、`exp002_kitagi_quarry_foss4g2026_poster.svg` |
| 手法・データ・結果・考察・限界・今後の課題 | `docs/reports/exp002_kitagi_quarry_water_detection_report.md` 3〜6章 |
| 春季プロベナンス | 同 4.1 追記（2026-08-14）、5.4 第6項 |
| 実装・出力先 | `notebooks/exp002_kitagi_quarry_water_detection.ipynb`、`scripts/generate_exp002_poster_figures.py` |
| 先行研究 | McFeeters 1996、Xu 2006、Du et al. 2016（ポスター References） |
