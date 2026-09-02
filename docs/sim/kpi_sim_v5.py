"""v5 model: 3-layer business (goal fixed at 1M take-home in 12 months).

Layer 1 (cash engine):   B2B retainers - SNS ops / short-video production for
                         wellness businesses (own faceless account = portfolio).
Layer 2 (asset engine):  faceless self-care media (v4 economics, reduced cadence
                         12 posts/month because time goes to Layer 1).
Layer 3 (leverage):      198,000 JPY 12-week habit program (from month 7, sold to
                         media audience, semi-personal: voice/name, no face) +
                         corporate one-off workshops (from month 9).

Assumes ~full commitment (30-40h/week). Success = 3-month rolling PROFIT >= 1.35M.
"""
import numpy as np

rng = np.random.default_rng(7)
N, M = 20000, 24
TARGET = 1_350_000
POSTS = 12                      # reduced cadence (time shared with client work)

# ---- Layer 2/3 media params (v4 economics) ----
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

# ---- Layer 1 B2B params ----
# new clients/month ~ Poisson(lam); lam = sales skill x proof effects
lam_base   = rng.lognormal(np.log(0.8), 0.5, N)        # median 0.8 new clients/mo at start
price0     = rng.normal(80_000, 20_000, N).clip(40_000, 140_000)   # first retainer price
price_grow = np.clip(rng.normal(1.04, 0.02, N), 1.00, 1.10)        # monthly price escalation (track record)
price_cap  = rng.normal(250_000, 60_000, N).clip(120_000, 450_000)
cap_seats  = rng.integers(4, 7, N)                      # capacity: 4-6 concurrent clients (solo + light outsourcing)
cl_churn   = np.clip(rng.normal(0.07, 0.03, N), 0.02, 0.15)
outsource_margin = 0.85                                 # editing outsourced at scale

# Layer 3
cvr_prog   = np.clip(rng.normal(0.0025, 0.0015, N), 0.0005, 0.006)  # reader -> 198k program
PRICE_PROG = 198_000
lam_ws     = rng.lognormal(np.log(0.4), 0.6, N)         # corporate workshops/mo from m9
PRICE_WS   = rng.normal(300_000, 80_000, N).clip(150_000, 500_000)

followers = np.zeros(N); members = np.zeros(N); shock_left = np.zeros(N, dtype=int)
clients = np.zeros(N)
profit = np.zeros((N, M + 1)); fol = np.zeros((N, M + 1))
b2b_r = np.zeros((N, M + 1)); med_r = np.zeros((N, M + 1)); prog_r = np.zeros((N, M + 1))

for m in range(1, M + 1):
    # ---- media growth ----
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

    r_med = np.zeros(N)
    if m >= 3:
        lineup = min(1 + (m - 3) / 1.5, 8)
        r_med += readers * cvr_paid * (0.4 + 0.6 * lineup / 8) * PRICE_NOTE * NET_NOTE
    if m >= 2:
        r_med += readers * cvr_aff * aff_payout
    if m >= 6:
        joins = readers * cvr_mem + (readers * cvr_paid * 0.08)
        members = members * (1 - churn) + joins
        r_med += members * PRICE_MEM * NET_MEM
    if m >= 3:
        usd = np.minimum(usd_base * usd_growth ** (m - 3), usd_cap)
        season = {11: 1.3, 0: 2.2, 1: 1.8}.get((8 + m) % 12, 1.0)
        r_med += usd * season * fx

    # ---- B2B retainers (sales start month 2; own account is the portfolio) ----
    r_b2b = np.zeros(N)
    if m >= 2:
        proof = (1 + 0.05 * (m - 2)) * (1 + 0.3 * np.log10(1 + followers / 1000))
        lam = lam_base * proof
        new_clients = rng.poisson(np.minimum(lam, 3.0))
        clients = np.minimum(clients * (1 - cl_churn) + new_clients, cap_seats)
        price_m = np.minimum(price0 * price_grow ** (m - 2), price_cap)
        r_b2b = clients * price_m * outsource_margin

    # ---- high-ticket program (m7+) & corporate workshops (m9+) ----
    r_prog = np.zeros(N)
    if m >= 7:
        r_prog += readers * cvr_prog * PRICE_PROG * 0.95
    if m >= 9:
        r_prog += rng.poisson(np.minimum(lam_ws, 2.0)) * PRICE_WS

    profit[:, m] = r_med + r_b2b + r_prog
    b2b_r[:, m], med_r[:, m], prog_r[:, m] = r_b2b, r_med, r_prog

def roll3(a, mm): return a[:, mm - 2:mm + 1].mean(axis=1)
def best_by(a, mm): return np.maximum.reduce([roll3(a, k) for k in range(4, mm + 1)])

r12 = roll3(profit, 12)
print("=== v5 三層モデル: 12ヶ月目 月利益（3ヶ月移動平均） ===")
for p in (10, 25, 50, 75, 90):
    print(f"  p{p}: {np.percentile(r12, p):,.0f}")
print("\n内訳（12ヶ月目中央値）: B2B受託 {:,.0f} / メディア {:,.0f} / 講座・研修 {:,.0f}".format(
    np.percentile(b2b_r[:, 12], 50), np.percentile(med_r[:, 12], 50), np.percentile(prog_r[:, 12], 50)))
print(f"稼働クライアント数12M 中央値: {np.percentile(clients, 50):.1f}社")
print("\n=== 手取り100万（月利益135万）達成確率 ===")
for mm in (12, 18, 24):
    print(f"  {mm}ヶ月以内: {(best_by(profit, mm) >= TARGET).mean() * 100:.1f}%")
print("\n=== 12ヶ月時点の水準別確率 ===")
for th, lbl in [(300_000, '30万'), (500_000, '50万'), (800_000, '80万'), (1_000_000, '100万')]:
    print(f"  月{lbl}以上: {(r12 >= th).mean() * 100:.1f}%")
print("\n=== マイルストーン整合（中央値） ===")
for mm in (3, 6):
    print(f"  {mm}ヶ月目 月利益: {np.percentile(profit[:, mm], 50):,.0f} "
          f"(B2B {np.percentile(b2b_r[:, mm], 50):,.0f} / メディア {np.percentile(med_r[:, mm], 50):,.0f})")
print("\n=== 感度分析: 12ヶ月以内に135万の条件付き確率 ===")
ok = best_by(profit, 12) >= TARGET
for cond, lbl in [
    (np.minimum(price0 * price_grow ** 10, price_cap) >= 150_000, "単価15万円以上に引き上げ成功"),
    (cap_seats >= 6, "外注化で6社同時運用"),
    (lam_base >= 1.0, "営業力: 新規獲得1社/月以上"),
    (fol[:, 12] >= 20000, "メディアがフォロワー2万超(営業の追い風)"),
]:
    print(f"  {lbl}: {ok[cond].mean() * 100:.1f}%  (該当率 {cond.mean() * 100:.0f}%)")
