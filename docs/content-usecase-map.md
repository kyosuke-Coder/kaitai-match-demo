# ユースケース型コンテンツマップ（AI検索時代対応）

作成日: 2026-09-02 / 対象: Tokyo Field Notes（英語Japanサイト）

## 方針：なぜ「ユースケース1つ＝1ページ」か

AI検索の普及で、クエリは「tokyo itinerary」のような単語型から、**条件付きの会話型**（"tokyo 4 days with a 3 year old in rainy season" のような）へ移行している。一般論の答え（アンサーワード）はAIが直接返してしまうが、**条件が2つ以上重なった瞬間、AIは信頼できる一次情報源を探して引用する**。そこに入り込むのがこのサイトの戦略。

- **1ユースケース＝1ページ**。「東京観光ガイド」のような総合ページは作らない
- **冒頭3行で答えを出す**（answer-first）。AIに引用されるのは結論が抽出しやすいページ
- 条件語彙で網を張る: *with kids / vegetarian / halal / rainy / in August / wheelchair / tattoo / solo female / on $100 a day / 8-hour layover / first time / no Japanese*

## AIO対応 記事テンプレート（全記事共通）

1. **TL;DR ボックス**（結論を3行・数字入りで冒頭に）
2. 比較・費用は必ず**表**にする（AIが抽出・引用しやすい構造）
3. **実測データを1つ以上**入れる（今月の価格・所要時間・写真＝このサイトにしかない情報）
4. **FAQ 3〜5問**（FAQPage schema付き）
5. 更新日を明示（"Verified September 2026"）+ Article schema
6. 記事末に該当する商品CTA（プランナー/チェックリスト）とメール登録

## コンテンツマトリクス（優先度順）

P1 = 購入意図高×競合弱×商品直結（最初の3ヶ月で制作） / P2 = 4〜6ヶ月 / P3 = 勝ちが見えたクラスタを拡張

### クラスタA: 旅程×条件（コア。プランナー直結）

| 想定クエリ（英語） | 条件 | 形式 | CTA | 優先 |
|---|---|---|---|---|
| tokyo 3 day itinerary first time | 初回 | ガイド | プランナー | **P1**（公開済み） |
| tokyo itinerary with toddler / kids | 子連れ | ガイド | 子連れ版チェックリスト | **P1** |
| tokyo rainy day itinerary | 雨 | ガイド | プランナー | **P1** |
| tokyo in august heat survival | 猛暑 | ガイド | 夏版パッキングリスト | P2 |
| tokyo itinerary for seniors slow pace | 高齢の親と | ガイド | プランナー | P2 |
| tokyo 8 hour layover haneda/narita | 乗継 | ガイド | ミニプランナー | **P1** |
| cherry blossom tokyo timing + where locals go | 桜 | ガイド(毎年更新) | 桜シーズナル版 | P2(1月公開) |
| is tokyo doable without japanese | 言語不安 | ガイド | フレーズカード | P2 |
| tokyo solo female traveler safety honest guide | 一人旅 | ガイド | プランナー | P2 |
| wheelchair accessible tokyo 3 days | 車椅子 | ガイド | プランナー | P3（競合ほぼゼロ・善意資産） |

### クラスタB: 食×制約（AI検索の会話型クエリが最多の領域）

| 想定クエリ | 条件 | 形式 | CTA | 優先 |
|---|---|---|---|---|
| vegetarian in tokyo (what locals suggest) | ベジ | ガイド+店リスト | 食制約フレーズカード | **P1** |
| halal food tokyo neighborhoods | ハラル | ガイド | 同上 | P2 |
| gluten free japan survival guide | GF | ガイド | 同上 | P2 |
| food allergy phrase card japanese | アレルギー | 無料DL+有料版 | **商品そのもの** | **P1**（リードマグネット） |
| kids picky eater japan restaurants | 子連れ×食 | ガイド | 子連れ版 | P3 |

### クラスタC: お金・仕組み（購入意図が最も強い）

| 想定クエリ | 形式 | CTA | 優先 |
|---|---|---|---|
| how much cash for 7 days in japan 2026 | ガイド+計算表 | 予算シート | **P1** |
| is the jr pass worth it 2026 | **計算ツール（自作）** | プランナー | **P1**（開発力の見せ場・被リンク獲得装置） |
| suica for tourists iphone setup | 手順ガイド | チェックリスト | **P1** |
| luggage forwarding takkyubin how to | 手順ガイド | プランナー | P2 |
| tax free shopping japan rules 2026 | ガイド | — | P2 |
| tipping in japan (short answer no, but…) | 短答ガイド | — | P3 |

### クラスタD: マナー・不安解消（「日本ならでは」の悩み）

| 想定クエリ | 形式 | CTA | 優先 |
|---|---|---|---|
| tattoos and onsen rules + tattoo friendly onsen tokyo | ガイド+リスト | 日帰り(箱根)ガイド | **P1**（会話型クエリの定番） |
| onsen etiquette first timer nervous | 手順ガイド | 同上 | P2 |
| train etiquette japan (what actually matters) | 短答ガイド | — | P3 |
| earthquake in japan as a tourist what to do | ガイド | — | P3（信頼構築・引用されやすい） |
| why no trash cans in japan + what to do | 短答ガイド | — | P3 |

### クラスタE: 日帰り（Tokyo-first戦略の外周）

| 想定クエリ | 形式 | CTA | 優先 |
|---|---|---|---|
| hakone or nikko which day trip | 比較表ガイド | 日帰りチートシート | **P1** |
| kamakura half day from tokyo | ガイド | 同上 | P2 |
| day trip from tokyo with kids | ガイド | 子連れ版 | P3 |

### クラスタF: 商品ページ連動（シーズナル）

- パッキングリスト4季節版（記事+無料1枚版→有料フル版）: 秋版をP1で先行（今が需要期）、冬・桜・夏を順次
- Cherry Blossom Planner（1月公開、3〜4月の季節山に照準）

## 制作カレンダーへの落とし込み

- 週2本ペース × 3ヶ月 = 24本 → **P1の13本を最初の7週で公開**、残りをP2から
- JR Pass計算ツールは土日2回分の開発枠で制作（10月中）。ツールは記事より寿命が長く、AI・人間両方から参照され続ける
- 毎月1回「価格・営業時間の検証散歩」（週末の一次情報収集）で既存記事のVerified日付を更新 — 更新日の新しさ自体がAIO優位

## 計測（ユースケース戦略専用のKPI）

- GSCで**条件語クエリのインプレッション比率**（"with kids" "vegetarian" 等を含むクエリ / 全体）を月次観測 — この比率が上がる＝戦略が刺さっている
- AI経由流入の代理指標: ダイレクト+リファラ不明の伸び、Perplexity/ChatGPT等のリファラ
- 記事別: 表示→クリック→商品ページ遷移→購入の4段ファネル（UTM）
