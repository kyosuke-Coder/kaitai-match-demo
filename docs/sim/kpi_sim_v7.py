"""v7 model: side-hustle digital EC + search/AIO-driven media (no client services).

Owner constraints: day job kept (local-store marketing => no client services, no
local-biz anything). ~20-30h/week (weeknights after 9pm + weekends, AI-assisted).
Layers:
  L1 digital EC: JP+EN templates/toolkits. Marketplace (Etsy/BOOTH/note) + own store.
     Price ladder: singles 1.5-3k -> bundles ~9.8k -> self-serve video toolkit 34,800 (m7+).
  L2 search/AIO media: SEO articles (owner is a pro) on AI-utilization/ops topics,
     ~9 articles/month with AI assist. Drives store + email list.
  L3 ads/affiliate on media (minor cash point) + email list.

Scenario A: stays side-hustle for 24 months.
Scenario B: goes full-time once 3-mo rolling profit >= 400k (output x1.8 thereafter).

Success = 3-month rolling profit >= 1.35M (take-home 1M).
"""
import numpy as np

rng = np.random.default_rng(21)
N, M = 20000, 24
TARGET = 1_350_000

# latent per-sim params
art_rate    = np.clip(rng.normal(9, 2, N), 5, 14)          # articles/month (side-hustle, AI-assisted)
sess_art    = rng.lognormal(np.log(120), 1.0, N)           # mature monthly sessions per article (pro SEO median 120)
aio_mult    = rng.lognormal(np.log(1.15), 0.2, N)          # AIO/AI-search citation skill bonus
serp_decay  = np.clip(rng.normal(0.985, 0.008, N), 0.955, 1.005)  # monthly headwind from AI answers
cvr_store   = np.clip(rng.normal(0.0035, 0.0015, N), 0.001, 0.008)  # session -> store purchase
aov0        = rng.normal(2500, 500, N).clip(1500, 4000)    # average order value at start
aov_grow    = np.clip(rng.normal(1.05, 0.02, N), 1.00, 1.12)   # bundles raise AOV, cap 2.2x
rpm_aff     = rng.lognormal(np.log(2000), 0.6, N)          # affiliate+ads JPY per 1k sessions
list_rate   = np.clip(rng.normal(0.015, 0.006, N), 0.005, 0.03)  # session -> email/LINE subscriber
crs_traffic = np.clip(rng.normal(0.0002, 0.0001, N), 0.00003, 0.0005)  # session -> 34.8k toolkit
crs_list    = np.clip(rng.normal(0.004, 0.002, N), 0.001, 0.010)        # list monthly -> toolkit
PRICE_CRS   = 34_800
# marketplace (Etsy/BOOTH): listings grow, sales/listing improves with reviews
lst_rate    = np.clip(rng.normal(3, 1, N), 1, 6)           # new listings/month
sales_lst   = rng.lognormal(np.log(0.4), 0.8, N)           # sales per listing per month (mature)
price_mkt   = rng.normal(1800, 400, N).clip(800, 3200)     # avg net-of-fees unit revenue (JPY, mixed JP/EN)
fx_season   = {11: 1.3, 0: 2.0, 1: 1.6}                    # Nov/Dec/Jan boost (start = September)

def run(fulltime_switch: bool):
    profit = np.zeros((N, M + 1))
    sessions_h = np.zeros((N, M + 1))
    arts = np.zeros(N); listings = np.zeros(N); subs = np.zeros(N)
    boost = np.ones(N)           # output multiplier (1.0 side-hustle, 1.8 after going full-time)
    shock_left = np.zeros(N, dtype=int)
    for m in range(1, M + 1):
        if fulltime_switch and m > 4:
            trig = profit[:, max(m - 3, 1):m].mean(axis=1) >= 400_000
            boost = np.where(trig, 1.8, boost)
        arts += art_rate * boost
        listings += lst_rate * boost

        # SEO traffic: articles mature over 6 months; algo shock like before
        algo_hit = rng.random(N) < 0.03
        shock_left = np.where(algo_hit, 3, np.maximum(shock_left - 1, 0))
        algo_mult = np.where(shock_left > 0, 0.6, 1.0)
        maturity = np.minimum(0.85, m / 12)   # cohort-blended maturity (newer articles not yet ranking)
        sessions = arts * sess_art * maturity * aio_mult * (serp_decay ** m) * algo_mult \
                   * rng.lognormal(0, 0.35, N)
        sessions_h[:, m] = sessions

        r = np.zeros(N)
        # own store EC
        aov = np.minimum(aov0 * aov_grow ** m, aov0 * 2.2)
        r += sessions * cvr_store * aov * 0.94          # payment fees
        # affiliate / ads on media (owner's original idea, kept as minor layer)
        r += sessions / 1000 * rpm_aff
        # marketplace
        season = fx_season.get((8 + m) % 12, 1.0)
        review_f = 1 + 0.04 * m
        r += listings * sales_lst * np.minimum(review_f, 2.0) * price_mkt * season * (m >= 2)
        # email list + 34,800 toolkit (from m7)
        subs = subs * 0.99 + sessions * list_rate
        if m >= 7:
            r += (sessions * crs_traffic + subs * crs_list) * PRICE_CRS * 0.92
        profit[:, m] = r
    return profit, sessions_h

def roll3(a, mm): return a[:, mm - 2:mm + 1].mean(axis=1)
def best_by(a, mm): return np.maximum.reduce([roll3(a, k) for k in range(4, mm + 1)])

for label, ft in [("A: 副業のまま24ヶ月", False), ("B: 月40万×3ヶ月で専業化スイッチ", True)]:
    p, sh = run(ft)
    r12 = roll3(p, 12)
    print(f"--- シナリオ{label} ---")
    print("  12ヶ月目 月利益 p25/p50/p75/p90: " +
          " / ".join(f"{np.percentile(r12, q):,.0f}" for q in (25, 50, 75, 90)))
    for mm in (12, 18, 24):
        print(f"  手取り100万 {mm}ヶ月以内: {(best_by(p, mm) >= TARGET).mean() * 100:.1f}%")
    for th, lbl in [(200_000, '20万'), (400_000, '40万'), (700_000, '70万')]:
        print(f"  12ヶ月時点 月{lbl}以上: {(r12 >= th).mean() * 100:.1f}%")
    print(f"  12ヶ月目セッション中央値: {np.percentile(sh[:, 12], 50):,.0f}/月")
    print(f"  3ヶ月/6ヶ月の月利益中央値: {np.percentile(p[:, 3], 50):,.0f} / {np.percentile(p[:, 6], 50):,.0f}")
    if ft:
        print(f"  専業化トリガー(月40万×3ヶ月)を24ヶ月内に踏む確率: "
              f"{(best_by(p, 24) >= 400_000).mean() * 100:.1f}%")
    print()

# sensitivity on scenario B
p, sh = run(True)
ok = best_by(p, 24) >= TARGET
print("=== 感度分析（シナリオB, 24ヶ月以内に135万の条件付き確率） ===")
for cond, lbl in [
    (sess_art >= 300, "記事あたり成熟セッション300以上(キーワード選定が当たる)"),
    (sess_art < 80, "同80未満(検索で拾えない)"),
    (rng.lognormal(np.log(150), 1.0, N) > 0, "(基準) 全体"),
]:
    print(f"  {lbl}: {ok[cond].mean() * 100:.1f}%  (該当率 {cond.mean() * 100:.0f}%)")
