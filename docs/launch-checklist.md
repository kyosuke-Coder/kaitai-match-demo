# ローンチチェックリスト（スタートに必要なもの一覧と手順）

最終更新: 2026-09-02 / ブランド: **Tokyo Field Notes**（朱色×クリーム白）

## 制作済みアセット（リポジトリ内・すぐ使える）

| アセット | 場所 | 用途 |
|---|---|---|
| 商品本体: Tokyo Travel Planner v0.2（10p PDF） | `products/tokyo-travel-planner/Tokyo-Travel-Planner-v0.2.pdf` | Etsy/Gumroad/自ストアで販売（$4.90→$7.90） |
| 無料版: Tokyo Cheat Sheet（1p PDF） | 同 `Tokyo-Cheat-Sheet-Free.pdf` | メール登録特典＋商品同梱（口コミ装置） |
| Pinterest ピン ×2（1000×1500） | 同 `marketing/pin1.png` `pin2.png` | ピン投稿（記事系・商品系の2型） |
| Etsyメイン画像（2000×1520） | 同 `marketing/etsy-main.png` | 出品1枚目 |
| Etsy出品文・タグ13個・価格戦略 | 同 `etsy-listing-draft.md` | コピペで出品 |
| 英語サイト一式（トップ/記事1本/About/開示） | `site/` | Cloudflare Pagesへデプロイ |
| ユースケース記事マップ（P1〜P3） | `docs/content-usecase-map.md` | 週2本の制作台本 |

※画像やPDFの再生成は各HTMLソースを編集→Chromiumで再レンダリング（このセッションでいつでも可能）。

## あなたがやること（順番どおり・所要目安）

### Step 0: 事前確認（30分・最重要）
- [ ] 就業規則の副業規定を確認
- [ ] ブランド名の最終決定（現案: Tokyo Field Notes。ドメイン・Etsyショップ名の空き確認とセットで）

### Step 1: 販売の土台（土日1日）
- [ ] ドメイン取得（tokyofieldnotes.com 等、年約1,500円）
- [ ] Etsyショップ開設（本人確認あり）→ Payoneer接続（外貨受け取り）
- [ ] 出品1点目: PDF+出品文+画像をアップ、$4.90でスタート
- [ ] Gumroadにも同商品を出品（第2販路・手数料のみ）

### Step 2: サイト公開（平日夜1〜2回）
- [ ] Cloudflare Pagesに `site/` をデプロイ（無料）
- [ ] GA4・GSC登録、サイトマップ送信
- [ ] メール配信（Brevo無料枠）開設 → Cheat Sheetを登録特典に配線
- [ ] サイトの「Get it on Etsy」リンクを実URLに差し替え

### Step 3: 集客の初速（翌週から通常運転）
- [ ] Pinterestビジネスアカウント開設 → pin1/pin2投稿＋週5ピンの型化
- [ ] Etsy内広告 $1/日でレビュー獲得を加速（最初の5レビューが目標）
- [ ] 週2本の記事制作をP1リスト順に開始（次: rainy day / layover / JR Pass計算ツール）

### Step 4: 2週間後の初計測
- [ ] Etsy: 表示→お気に入り→購入 / Pinterest: 表示→クリック
- [ ] GSC: 条件語クエリのインプレッション
- [ ] 数字を持って次の一手を決める（商品2号 or 記事増産 or 価格調整）

## 判断済みの設計（迷ったらここに戻る）

- 商品名は **Tokyo** 軸（中身がTokyo-firstのため）。ブランドも東京で立てる
- デザイン: 赤白は維持しつつ日の丸そのものにしない — **朱色(#d5573b)×クリーム(#fdf8f2)＋丸み＋小さな東京モチーフ**が公式トーン
- 集客の主戦場は Etsy内検索＋Pinterest＋商品。ブログは「AIに引用される一次情報」とリスト獲得の装置
- 価格: $4.90（レビュー20件まで）→ $7.90 → シーズナル版とバンドル$14.90
