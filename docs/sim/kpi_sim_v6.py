"""v6 model: own-service only (no agency work).

Layer 1 (cash engine):  own D2C program - 12-week sleep/autonomic self-care
                        coaching program, 198,000 JPY. Monitors m2-3, sales from m4.
                        High ticket => paid ads become viable (the organic ceiling breaks).
Layer 2 (lead engine):  faceless self-care media (15 posts/mo) + note products + USD templates.
Layer 3 (scale asset):  habit-tracking LINE app (own dev skill), B2C sub 1,480 JPY from m10.

Success = 3-month rolling profit >= 1.35M.
"""
import numpy as np

rng = np.random.default_rng(11)
N, M = 20000, 24
TARGET = 1_350_000
POSTS = 15

# media (v4 economics)
fpp_base   = rng.lognormal(np.log(25), 0.9, N)
cvr_paid   = np.clip(rng.normal(0.020, 0.007, N), 0.005, 0.045)
cvr_mem    = np.clip(rng.normal(0.008, 0.004, N), 0.002, 0.020)
churn      = np.clip(rng.normal(0.06, 0.02, N), 0.03, 0.12)
cvr_aff    = np.clip(rng.normal(0.012, 0.005, N), 0.003, 0.030)
aff_payout = rng.normal(6000, 1200, N).clip(3000, 10000)
usd_base   = rng.lognormal(np.log(80), 0.8, N)
usd_growth = np.clip(rng.normal(1.22, 0.08, N), 1.05, 1.45)
usd_cap    = rng.lognormal(np.log(1200), 0.6, N)
fx         = rng.normal(150, 10, N).clip(120, 180)
PRICE_NOTE, NET_NOTE = 1980, 0.82
PRICE_MEM,  NET_MEM  = 1480, 0.80

# Layer 1: program
PRICE_PROG   = 198_000
NET_PROG     = 0.90                                   # payment fees + 5% refunds
cvr_consult  = np.clip(rng.normal(0.012, 0.006, N), 0.003, 0.030)   # reader -> free consult booking
close        = np.clip(rng.normal(0.25, 0.07, N), 0.10, 0.40)       # consult -> enrollment
cpa_consult  = rng.lognormal(np.log(10_000), 0.4, N)                # ad cost per consult booking
cap_enroll   = np.clip(rng.normal(9, 2, N), 5, 14)                  # delivery capacity (solo, weekly sessions)
ads_viable   = PRICE_PROG * NET_PROG * close * 0.85 > 2.5 * cpa_consult   # CAC < ~40% of price

# Layer 3: app
subs = np.zeros(N)
APP_PRICE, APP_NET, app_churn = 1480, 0.85, 0.07

followers = np.zeros(N); members = np.zeros(N); shock_left = np.zeros(N, dtype=int)
profit = np.zeros((N, M + 1)); fol = np.zeros((N, M + 1))
prog_r = np.zeros((N, M + 1)); med_r = np.zeros((N, M + 1)); app_r = np.zeros((N, M + 1))
spend_hist = np.zeros((N, M + 1))

for m in range(1, M + 1):
    monthly_shock = rng.lognormal(0, 0.5, N)
    algo_hit = rng.random(N) < 0.03
    shock_left = np.where(algo_hit, 3, np.maximum(shock_left - 1, 0))
    algo_mult = np.where(shock_left > 0, 0.5, 1.0)
    gf = 1 + 0.6 * np.log10(1 + followers / 1000)
    new_f = POSTS * fpp_base * gf * monthly_shock * algo_mult
    new_f += (rng.random(N) < 0.05 * POSTS / 20) * rng.lognormal(np.log(3000), 0.7, N)
    followers += new_f; fol[:, m] = followers

    readers = (0.20 * new_f + 0.020 * followers) * rng.lognormal(0, 0.3, N)
    if m >= 6: readers *= 1.2

    # media revenue
    r_med = np.zeros(N)
    if m >= 3:
        lineup = min(1 + (m - 3) / 1.5, 8)
        r_med += readers * cvr_paid * (0.4 + 0.6 * lineup / 8) * PRICE_NOTE * NET_NOTE
    if m >= 2:
        r_med += readers * cvr_aff * aff_payout
    if m >= 6:
        members = members * (1 - churn) + readers * cvr_mem + readers * cvr_paid * 0.08
        r_med += members * PRICE_MEM * NET_MEM
    if m >= 3:
        usd = np.minimum(usd_base * usd_growth ** (m - 3), usd_cap)
        season = {11: 1.3, 0: 2.2, 1: 1.8}.get((8 + m) % 12, 1.0)
        r_med += usd * season * fx

    # program (sales from m4; monitors before that build cases)
    r_prog = np.zeros(N); ad_spend = np.zeros(N)
    if m >= 4:
        consults = readers * cvr_consult
        if m >= 6:
            ad_spend = np.where(ads_viable, np.minimum(0.35 * np.maximum(profit[:, m - 1], 0), 1_200_000), 6000)
            consults = consults + (ad_spend / cpa_consult) * 0.85   # ad-sourced consults close slightly worse via same rate applied below
        enroll = np.minimum(consults * close, cap_enroll)
        r_prog = enroll * PRICE_PROG * NET_PROG

    # app (from m10): joins from program grads + readers
    r_app = np.zeros(N)
    if m >= 10:
        subs = subs * (1 - app_churn) + np.minimum(readers * 0.002, 200) + 2.0
        r_app = subs * APP_PRICE * APP_NET

    profit[:, m] = r_med + r_prog + r_app - ad_spend
    prog_r[:, m], med_r[:, m], app_r[:, m] = r_prog - ad_spend, r_med, r_app
    spend_hist[:, m] = ad_spend

def roll3(a, mm): return a[:, mm - 2:mm + 1].mean(axis=1)
def best_by(a, mm): return np.maximum.reduce([roll3(a, k) for k in range(4, mm + 1)])

r12 = roll3(profit, 12)
print("=== v6 自社サービスモデル: 12ヶ月目 月利益（3ヶ月移動平均） ===")
for p in (10, 25, 50, 75, 90):
    print(f"  p{p}: {np.percentile(r12, p):,.0f}")
print("\n内訳（12ヶ月目中央値）: プログラム(広告費差引後) {:,.0f} / メディア {:,.0f} / アプリ {:,.0f} / 広告費 {:,.0f}".format(
    np.percentile(prog_r[:, 12], 50), np.percentile(med_r[:, 12], 50),
    np.percentile(app_r[:, 12], 50), np.percentile(spend_hist[:, 12], 50)))
print(f"広告ユニットエコノミクス成立率: {ads_viable.mean()*100:.1f}%")
print("\n=== 手取り100万（月利益135万）達成確率 ===")
for mm in (12, 18, 24):
    print(f"  {mm}ヶ月以内: {(best_by(profit, mm) >= TARGET).mean() * 100:.1f}%")
print("\n=== 12ヶ月時点の水準別確率 ===")
for th, lbl in [(300_000, '30万'), (500_000, '50万'), (800_000, '80万'), (1_350_000, '135万')]:
    print(f"  月{lbl}以上: {(r12 >= th).mean() * 100:.1f}%")
print("\n=== マイルストーン（中央値） ===")
for mm in (3, 6, 9):
    print(f"  {mm}ヶ月目 月利益: {np.percentile(profit[:, mm], 50):,.0f} "
          f"(プログラム {np.percentile(prog_r[:, mm], 50):,.0f} / メディア {np.percentile(med_r[:, mm], 50):,.0f})")
print("\n=== 感度分析: 12ヶ月以内135万の条件付き確率 ===")
ok = best_by(profit, 12) >= TARGET
for cond, lbl in [
    (ads_viable, "広告経済性が成立(CAC<価格の40%)"),
    (close >= 0.30, "成約率30%以上"),
    (fol[:, 12] >= 20000, "フォロワー2万超"),
    (cap_enroll >= 11, "提供キャパ月11件以上(グループ化等)"),
]:
    print(f"  {lbl}: {ok[cond].mean() * 100:.1f}%  (該当率 {cond.mean() * 100:.0f}%)")
