# FOSS4G Hiroshima 2026 ポスター 口頭説明スクリプト（英日併記）

対象ポスター: `exp002_kitagi_quarry_foss4g2026_poster.pdf` — *Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools* / Noboru Otsuka (Geolonia Inc.)

> **前提訂正（2026-08-23）**: 本発表の採択形式は**ポスターではなく口頭発表**（Regular Talk）である。
> **2026-09-02 13:30–14:00、Himawari、発表20分＋質疑5分、英語**。根拠は主催者メール3通と公式
> スケジュール（`schedule.json` v0.27）で、記録は Issue #6 #issuecomment-5385220162 および
> `docs/posters/exp002_kitagi_foss4g2026_proposal.md`「発表形式（2026-08-23 確定）」を参照。
> ポスター掲出・コアタイムを前提とした本書の運用記述は**廃止**した（§5 参照）。
>
> 本書のうち引き続き有効なのは、チートシート（§0）・30秒版・2〜3分版・5分版（廊下や休憩時間の
> 会話用）・定型フレーズ・出典である。スライドの正本は
> `docs/presentations/exp002_kitagi_foss4g2026_presentation.md`、発表後の質疑には
> `exp002_kitagi_foss4g2026_qa.md` を使う。

想定質問への回答は `exp002_kitagi_foss4g2026_qa.md` を参照。

---

## 0. チートシート

### 0-1. 1画面カード（スマートフォンでこれだけ見る）

- **113 / 145** = detected water polygons（春 / 夏）。**candidates — not field-confirmed**
- **127** = 1957年ピークの稼働丁場数。145との比較は **scale only, not one-to-one**
- **10 m** 解像度 ／ **100 m²** 下限 — これが検出限界
- 閾値: **NDWI > −0.2 or MNDWI > −0.1、NDVI > 0.3 は除外**（負の閾値はスペクトル混合対策）
- **精度指標なし**（現地検証未実施）。断定を求められたら “I can't confirm any individual pond.”
- 春季 **113** は当時の報告値。現行パイプラインでは別の値になり、**差の原因は特定できていない**
- QR = コード・レポート・ポスター・**夏季145ポリゴンの GeoJSON**
- ライセンス: 本発表は **CC BY 4.0**。Sentinel画像とGSI基図は各自の条件

### 0-2. 使ってよい数値（Tier 1 = ポスターに掲載されている値すべて）

| 値 | 意味 |
|---|---|
| **113** | 春季（2025-03-23）に検出した島内水域ポリゴン数（100 m² 以上） |
| **145** | 夏季（2025-08-02）に検出した島内水域ポリゴン数（100 m² 以上） |
| **127** | 1957年（昭和32年）ピーク時に記録された稼働丁場数（歴史的文脈。検出数との1対1対応ではない） |
| **9 px** | 夏季で NDVI 植生マスクにより除外されたピクセル数 |
| **100 m²** | ポリゴン抽出の最小面積 |
| **10 m** | Sentinel-2 の解析グリッド解像度（検出限界の主要因） |
| **2025-03-23 / 2025-08-02** | 春季 / 夏季シーンの撮影日 |
| **−0.2 / −0.1 / 0.3** | NDWI / MNDWI / NDVI の閾値 |
| **0.0% / 0.7%** | 春季 / 夏季シーンの雲量 |
| **20 m** | B11（SWIR）のネイティブ解像度。10 mグリッドへリサンプリング |

**Tier 1 の定義**: ポスターに掲載されている値はすべて Tier 1 で、どのバージョンでも使える。上表はその主要な抜粋であり、網羅列挙ではない（表に無くてもポスターに載っていれば Tier 1）。

**Tier 2**: ポスターに無く報告書のみに基づく補足値（現行パイプライン再計算の 180、最大水域 7,826 m²、植生マスク 72,636 px、丁場跡の水深、シーンID 等）。**5分版と想定問答でのみ**使用し、同一行に `[report]` / `[報告書]` の出典マーカーを付ける。マーカーは原稿上の注記であり、読み上げない（口頭では「報告書の値ですが」と添える）。

**Tier 3**: 報告書の推定・可能性の記述（検出最大ポリゴンが「北木の桂林」に相当するというOSM照合に基づく対応づけなど）。報告書と同じ *may / possibly* のヘッジを外さない。

### 0-3. 言ってはいけない / 言い換える表現

| ✗ 言わない | ✓ 言う |
|---|---|
| “We found 145 quarry ponds.” | “We detected 145 water polygons — quarry pond **candidates**.” |
| “We confirmed the ponds are former quarries.” | “Their distribution is **consistent with** the quarrying history.” |
| “145 of the 127 quarries…” | “A **scale** comparison, not a one-to-one match.” |
| “Accuracy is high.” | “We have **no accuracy metrics yet** — that needs field validation.” |
| “The NDVI mask improved accuracy.” | “The NDVI mask excluded only 9 pixels — its effect was **limited** here.” |
| （春季について）“113 is reproducible.” | “113 is our reported figure; the exact historical run configuration **is not preserved**.” |

### 0-4. ポスターの指差しマップ

| 位置 | 内容 |
|---|---|
| **上部バンド** | タイトル・著者・一文サマリ |
| **左カラム** | ① Background and heritage（**127** 大文字カウント）→ ② Research question → F1 位置図 → ③ Data and study area → F6 現地写真（Choba lake） |
| **中央カラム** | ④ Method（4ステップの流れ図・3つの式・複合条件）→ F4 指数パネル → **10 m** カウント → 9 px の記述 → F5 水域強調画像 |
| **右カラム** | ⑤ Results（**113 / 145** の数値タイル・春季注記）→ F3 夏季検出地図 → ⑥ Interpretation and limitations → Conclusion and reuse |
| **フッター** | References ／ Attribution and license（CC BY 4.0・Copernicus）／ QR: github.com/mopinfish/geo-laboratory |

---

## 1. 30秒版 — 通りがかりの聴衆向け

立ち止まった人に、**タイトル → 何をしたか → 数字 → 留保**の順で渡す。指差しは右カラムの 113 / 145 タイルのみ。

### English（実測 75 words / 約 31 秒。以下 145 wpm 換算）

> This poster is about Kitagi Island in Japan's Seto Inland Sea — a granite quarrying island with 127 active quarry sites at its 1957 peak. Abandoned pits filled with water, but there was no systematic spatial inventory of them. With free Sentinel-2 imagery and open-source Python tools, we detected 113 water polygons in spring and 145 in summer, each at least 100 square metres. The pattern matches the island's quarrying history — but these are candidates; individual ponds are not field-validated yet.

### 日本語

> 瀬戸内海の北木島という花崗岩の採石島を対象にした研究です。1957年のピーク時には127か所の丁場が稼働していました。廃業した丁場跡には水が溜まって池になっていますが、その体系的な空間インベントリは作られていませんでした。無償のSentinel-2画像とオープンソースのPythonツールで、春季に113、夏季に145の水域ポリゴン（各100 m²以上）を検出しました。分布は採石の歴史と整合します。ただしこれらは候補であり、個々の池の現地検証はまだ行っていません。

**この後の分岐**: 相手が質問なしで離れる → “The code, the report, and the detected polygons as GeoJSON are on the QR at the bottom.” ／ 相手が残る → 2〜3分版の 3.（データ）から続ける。

---

## 2. 2〜3分版 — コアタイムの標準

6ビート構成。各ビートの冒頭に指差し先を示す。英文計 405 words / 約 2分48秒。

### Beat 1 — 遺産としての島（左カラム ①、**127** を指す）

**EN:** Kitagi Island is in the Seto Inland Sea, in Okayama Prefecture. It has been quarried for granite since the early seventeenth century, and at the 1957 peak the records list 127 active quarry sites — locally called *dojo*. When the industry declined, the abandoned excavations filled with rainwater and groundwater, so today the island holds isolated ponds walled in by vertical granite faces. The stone culture became national heritage in 2019.

**JP:** 北木島は岡山県笠岡市、瀬戸内海の島です。17世紀初頭から花崗岩の採石が続き、1957年のピーク時には127か所の丁場（ちょうば）が稼働していたと記録されています。産業の衰退後、放棄された採石跡に雨水や地下水が溜まり、垂直な花崗岩の壁に囲まれた孤立した池が残りました。2019年には島の石の文化が日本遺産に認定されています。

### Beat 2 — 問い（左カラム ②、F1 位置図）

**EN:** But there was no systematic spatial inventory of those ponds. So the question is simple: can open satellite imagery and reproducible open-source tools map the water bodies associated with former quarry sites — and do their spatial patterns correspond to the island's quarrying history?

**JP:** しかし、これらの池を網羅的に地図化したものはありませんでした。そこで問いは単純です。オープンな衛星画像と再現可能なオープンソースツールで、丁場跡に関連する水域を地図化できるか。そしてその空間分布は、島の採石の歴史と対応するか。

### Beat 3 — データ（左カラム ③、必要なら F6 現地写真）

**EN:** I used Sentinel-2 Level-2A imagery, accessed through the Microsoft Planetary Computer STAC API — no data purchase, no local archive. Two scenes: spring, 2025-03-23, with zero percent cloud, and summer, 2025-08-02, with 0.7 percent. Everything runs on a 10-metre analysis grid, and I only report polygons of 100 square metres or larger.

**JP:** データはSentinel-2 L2Aで、Microsoft Planetary ComputerのSTAC API経由で取得しています。データ購入もローカルアーカイブも不要です。シーンは2つ、春季が2025年3月23日（雲量0.0%）、夏季が2025年8月2日（雲量0.7%）。解析は10 mグリッド、報告するのは100 m²以上のポリゴンのみです。

### Beat 4 — 手法（中央カラム ④ の流れ図 → 式 → F4）

**EN:** The pipeline is four steps: STAC search, band access, a water-index union, then a vegetation mask and polygon extraction. I use NDWI from green and near-infrared, MNDWI from green and short-wave infrared, and NDVI to mask vegetation. A pixel is water if NDWI is above minus 0.2 **or** MNDWI is above minus 0.1, and NDVI is not above 0.3. The thresholds are negative on purpose: at 10 metres, small ponds are spectrally mixed with the surrounding rock, so a textbook threshold of zero would simply miss them.

**JP:** パイプラインは4ステップです。STAC検索、バンド取得、水域指数の和集合、そして植生マスクとポリゴン抽出。指数はNDWI（緑・近赤外）、MNDWI（緑・短波赤外）、そして植生マスク用のNDVI。判定は「NDWI > −0.2 または MNDWI > −0.1、かつ NDVI > 0.3 でない」です。閾値を意図的に負にしているのがポイントで、10 m解像度では小さな池が周囲の岩肌とスペクトル混合するため、教科書的な0という閾値では取りこぼしてしまいます。

### Beat 5 — 結果（右カラム ⑤ の 113 / 145 タイル → F3）

**EN:** Spring gave 113 intra-island water polygons; summer gave 145. The summer detections cluster in the north, the south-east, the centre and the west — and that is a pattern consistent with the historical quarrying records, where the north side was the industrial core. One honest caveat right here: these are detected water polygons, not individually field-confirmed quarry ponds. Natural ponds, irrigation reservoirs and shadows can still be in there.

**JP:** 春季で島内113、夏季で145のポリゴンを検出しました。夏季の検出は北部・南東部・中央部・西部の4か所に集中していて、これは採石の中心が島の北側だったという歴史的記録と整合するパターンです。ここで正直に留保を一つ。これらは検出された水域ポリゴンであって、個別に現地確認された丁場池ではありません。自然の池沼、農業用ため池、影などが含まれている可能性があります。

### Beat 6 — 限界と持ち帰り（右カラム ⑥ → Conclusion → フッターQR）

**EN:** So the limits: 10-metre resolution and spectral mixing, negative thresholds that can pick up dark rock or shadow, and no accuracy metrics until we go to the field. The 145-to-127 comparison is a comparison of scale, not a one-to-one match. What I claim is narrower and, I think, still useful: a lightweight, reproducible workflow that produces a first spatial inventory of quarry-pond candidates — GeoJSON and GeoTIFF you can take into the field. It should transfer to the other quarried islands in the Seto Inland Sea. The code, the report and the 145-polygon GeoJSON are behind the QR code.

**JP:** 限界としては、10 m解像度とスペクトル混合、負の閾値による暗い岩肌や影の誤検出リスク、そして現地に行くまで精度指標が出せないこと。145と127の比較は規模の比較であって、1対1の対応ではありません。主張はもっと控えめですが有用だと考えています。軽量で再現可能なワークフローが、丁場池候補の最初の空間インベントリを作る。GeoJSONとGeoTIFFで出力しているので、そのまま現地調査に持ち出せます。瀬戸内海の他の採石島にも展開できるはずです。コード・レポート・145ポリゴンのGeoJSONは下のQRから。

---

## 3. 5分版 — 詳細に関心のある聴衆向け

2〜3分版の6ビートに、下記4ビートを差し込む。挿入分364 wordsを含め英文計 769 words / 約 5分18秒。

### Beat 3.5 — 現地の実感（Beat 3 の後。左カラム F6 写真）

**EN:** These are my own photographs from the island. You can see what the target actually looks like: a flooded pit with sheer granite walls; the reported depths run from a few metres to about twenty `[report]`, and the water takes on an unusual green. Two things matter for the remote sensing. The walls shadow the water surface, and the ponds are small and irregular — which is exactly why the index values come out low.

**JP:** これは私が現地で撮った写真です。対象が実際にどういうものか分かると思います。垂直な花崗岩の壁に囲まれた水没した採石跡で、深さは数mから20m程度と記録されており `[報告書]`、水は独特の緑色を帯びます。リモートセンシング上重要な点が2つあります。壁が水面に影を落とすこと、そして池が小さく不整形であること。だから指数値が低く出るのです。

### Beat 4.5 — NDVIマスクの「意外な結果」（Beat 4 の後。中央カラムの 9 px と F4）

**EN:** One result surprised me. I expected the NDVI vegetation mask to do real work in summer — that was my third hypothesis. It excluded **nine pixels**. Nine. So in this scene the water candidates and the vegetated areas barely overlapped in this granite-dominated landscape. That hypothesis is rejected, and I keep the mask as a low-cost safeguard for transferring the workflow to greener islands.

**JP:** 一つ意外な結果がありました。夏季ではNDVI植生マスクが効くと予想していた — これが3番目の仮説でした。実際に除外されたのは**9ピクセル**です。9です。つまり花崗岩が卓越するこのシーンでは、水域候補と高NDVI植生域の重複がほとんどなかったということです。この仮説は棄却されました。マスクは、より緑の多い島へワークフローを展開するときの低コストな安全策として残しています。

### Beat 5.5 — 季節差の読み方（Beat 5 の後。右カラム 113 / 145 タイルと春季注記）

**EN:** The seasonal difference is not simply "summer is better". Spring has a much wider index range and finds the large ponds well; summer returns more polygons and is better at the small ones. Three plausible reasons for the narrower summer range — atmospheric water vapour, warmer and more turbid seawater, and a higher solar elevation angle changing the reflection at the surface. I have not separated those, so I treat the two dates as two different observations, not interchangeable ones. And note the line under the tile: 113 is the figure reported from our March 2026 run. That run's exact configuration was not preserved, re-running the current pipeline on the same scene gives 180 `[report]`, and we have not isolated where the difference comes from — I'm happy to go into that if you want the details.

**JP:** 季節差は単純に「夏が良い」という話ではありません。春季は指数の値域が広く大型水域の検出に優れ、夏季はポリゴン総数が多く小規模水域に強い。夏季の値域が狭い理由としては、大気の水蒸気量、海水温上昇と懸濁物質、太陽高度角による水面反射の違いの3つが考えられます。これらを分離できていないので、2時期は「入れ替え可能な観測」ではなく「別の観測」として扱っています。それとタイル下の注記ですが、113は2026年3月の実行で報告した値です。当時の設定が保存されておらず、同じシーンに現行パイプラインを適用すると180になります `[報告書]`。差がどこから来ているかは特定できていません。詳しく聞きたければ説明します。

### Beat 6.5 — 再現性と次の一手（Beat 6 の直前。中央カラム F5 → フッター）

**EN:** On reproducibility: the whole stack is open — rasterio, numpy, shapely, pystac-client, planetary-computer and folium — no licensed software anywhere in the chain, and the imagery is free. Outputs are GeoJSON and GeoTIFF, so the next step is concrete: take the candidate layer to the island, check the polygons against known quarry locations, and finally compute precision and recall. After that, a strict land mask to remove coastal artefacts, and higher-resolution imagery for the ponds below 100 square metres. This conference contribution is CC BY 4.0; the Sentinel imagery and the GSI basemap retain their own terms and attribution.

**JP:** 再現性について。スタックは全てオープンです — rasterio、numpy、shapely、pystac-client、planetary-computer、folium。有償ソフトは一切なく、画像も無償です。出力はGeoJSONとGeoTIFFなので、次の一手は具体的です。候補レイヤを島に持ち込み、既知の丁場位置と照合して、適合率・再現率を算出する。その後、海岸線のアーティファクトを除く厳密な陸域マスク、そして100 m²未満の池のための高分解能画像。本発表はCC BY 4.0です。Sentinel画像とGSI基図はそれぞれの条件と帰属表示が必要です。

---

## 4. 定型フレーズ

### 声かけ・導入

- “Would you like the thirty-second version or the longer one?”（時間の主導権を相手に渡す）
- “Do you work with satellite imagery yourself?”（相手の背景で説明の深さを決める）
- 日本語話者と分かった場合: 「日本語でも大丈夫です」（ポスター自体は英語のまま説明できる）

### 答えられないとき（そのまま使う）

- **EN:** “I don't have that measured — I'd be overclaiming if I answered. It's on the list for the field campaign.”
- **JP:** 「それは計測していないので、答えると過大主張になります。現地調査の項目に入れています。」
- **EN:** “Good question — can I take your contact and follow up with the actual number?”
- **JP:** 「良い質問です。連絡先をいただいて、実際の数字をお送りしてもよいですか。」

### 締め

- **EN:** “The code, the report, the poster and the 145-polygon GeoJSON are all under the QR at the bottom. This contribution is CC BY 4.0; the Sentinel imagery and the GSI basemap keep their own terms.”
- **JP:** 「コード・レポート・ポスター・145ポリゴンのGeoJSONはすべて下のQRから。本発表はCC BY 4.0です。Sentinel画像とGSI基図はそれぞれの条件に従ってください。」

---

## 5. 運用メモ

**廃止した記述（2026-08-23）**: 旧版はポスター掲出（Sakura Lounge、9月1〜3日）とコアタイム（9月2日 13:00–15:00）を前提に、Himawari 枠での在席要否を未確認事項としていた。採択形式が口頭発表と確定したため、これらの前提はすべて無効である。Himawari 枠は本発表そのものの登壇枠であり、在席要否という論点は存在しない。

**現行の運用**:

- 登壇は **9月2日 13:30–14:00、Himawari**。発表20分・質疑5分・入替5分。使用言語は英語
- 本書の30秒版・2〜3分版・5分版は、廊下・休憩時間・懇親会での会話用として使う。登壇本体のスクリプトは `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md`
- 登壇後の質疑5分には想定問答（`exp002_kitagi_foss4g2026_qa.md`）を使う。スマートフォンで開ける状態にしておく
- 同日 17:30 に別会場（Dahlia1）で別発表があるため、質疑後の移動時間を確保する

---

## 6. 出典

| 記述 | 出典 |
|---|---|
| 全ての Tier 1 数値・主張・留保文言 | `exp002_kitagi_quarry_foss4g2026_poster_content.md`（内容契約）、`exp002_kitagi_quarry_foss4g2026_poster.svg`（最終文言） |
| 4か所の集中地帯、北部が採石中心 | `docs/reports/exp002_kitagi_quarry_water_detection_report.md` 4.3、5.3 |
| NDVIマスク仮説の棄却（9 px） | 同 5.1 仮説3 |
| 夏季の指数値域が狭い3つの要因 | 同 5.2 |
| 春季113のプロベナンス | 同 4.1 追記（2026-08-14）、5.4 第6項 |
| 春季・夏季の検出特性の違い | 同 4.4 |
| 今後の課題（陸域マスク・現地検証・高分解能） | 同 6.3 |
| 現地写真の内容（水深数m〜20 m・緑色の水） | 同 1.1、5.3、`docs/results/exp002/photos/` |
| 公開した夏季145ポリゴンのGeoJSON | `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`（生成: `scripts/generate_exp002_poster_figures.py`、注意書き: 同ディレクトリの `_README.md`） |
