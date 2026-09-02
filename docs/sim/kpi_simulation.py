"""Scenario comparison:
A) organic only (v3 plan as-is)
B) organic + ad-reinvestment loop from month 6:
   reinvest 25% of prior-month profit into Meta/TikTok ads ONLY while unit economics pass
   (LTV per note-reader > 1.3x cost per ad-acquired reader). Ad spend is variable cost,
   outside the 8,000 JPY fixed-cost cap. Success metric = monthly PROFIT (rev - ads) >= 1.35M.
"""
import numpy as np

rng = np.random.default_rng(42)
N, M = 20000, 24
TARGET, POSTS = 1_350_000, 20

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
cpr        = rng.lognormal(np.log(250), 0.4, N)   # ad cost per acquired note-reader (JPY)

PRICE_NOTE, NET_NOTE = 1650, 0.82
PRICE_MEM,  NET_MEM  = 980, 0.80
PRICE_MID,  NET_MID  = 7000, 0.80

# LTV of one organic note reader (used for ad viability gate; ad readers monetize at 0.7x)
ltv_reader = (cvr_paid * 0.9 * PRICE_NOTE * NET_NOTE
              + cvr_mem * PRICE_MEM * NET_MEM / churn
              + cvr_aff * aff_payout
              + 0.003 * PRICE_MID * NET_MID)
viable = ltv_reader * 0.7 > 1.3 * cpr

def run(with_ads: bool):
    followers = np.zeros(N); members = np.zeros(N); shock_left = np.zeros(N, dtype=int)
    profit = np.zeros((N, M + 1)); fol = np.zeros((N, M + 1))
    for m in range(1, M + 1):
        monthly_shock = rng.lognormal(0, 0.5, N)
        algo_hit = rng.random(N) < 0.03
        shock_left = np.where(algo_hit, 3, np.maximum(shock_left - 1, 0))
        algo_mult = np.where(shock_left > 0, 0.5, 1.0)
        gf = 1 + 0.6 * np.log10(1 + followers / 1000)
        new_f = POSTS * fpp_base * gf * monthly_shock * algo_mult
        new_f += (rng.random(N) < 0.05) * rng.lognormal(np.log(3000), 0.7, N)
        followers += new_f; fol[:, m] = followers

        readers = (0.12 * new_f + 0.015 * followers) * rng.lognormal(0, 0.3, N)
        if m >= 6: readers *= 1.2

        ad_spend = np.zeros(N); ad_readers = np.zeros(N)
        if with_ads and m >= 6:
            ad_spend = np.where(viable, 0.25 * np.maximum(profit[:, m - 1], 0), 6000)
            ad_readers = ad_spend / cpr

        def monetize(rd, mult):
            r = np.zeros(N)
            if m >= 3:
                lineup = min(1 + (m - 3) / 1.5, 8)
                r += rd * cvr_paid * mult * (0.4 + 0.6 * lineup / 8) * PRICE_NOTE * NET_NOTE
            if m >= 2:
                r += rd * cvr_aff * mult * aff_payout
            if m >= 9:
                r += rd * 0.003 * mult * PRICE_MID * NET_MID
            return r

        r = monetize(readers, 1.0) + monetize(ad_readers, 0.7)
        if m >= 6:
            joins = (readers + 0.7 * ad_readers) * cvr_mem
            if m >= 3: joins += (readers + 0.7 * ad_readers) * cvr_paid * 0.08
            members = members * (1 - churn) + joins
            r += members * PRICE_MEM * NET_MEM
        if m >= 3:
            usd = np.minimum(usd_base * usd_growth ** (m - 3), usd_cap)
            season = {11: 1.3, 0: 2.2, 1: 1.8}.get((8 + m) % 12, 1.0)
            r += usd * season * fx
        profit[:, m] = r - ad_spend
    return profit, fol

def roll3(a, m): return a[:, m - 2:m + 1].mean(axis=1)
def best_by(a, mm): return np.maximum.reduce([roll3(a, k) for k in range(4, mm + 1)])

for label, with_ads in [("A: オーガニックのみ", False), ("B: 広告再投資ループあり", True)]:
    p, fol = run(with_ads)
    r12 = roll3(p, 12)
    print(f"--- シナリオ{label} ---")
    print("  12ヶ月目 月利益 p50/p75/p90:",
          " / ".join(f"{np.percentile(r12, q):,.0f}" for q in (50, 75, 90)))
    for mm in (12, 18, 24):
        print(f"  手取り100万(月利益135万) {mm}ヶ月以内: {(best_by(p, mm) >= TARGET).mean()*100:.1f}%")
    for th, lbl in [(200_000, '20万'), (500_000, '50万')]:
        print(f"  12ヶ月時点 月{lbl}以上: {(r12 >= th).mean()*100:.1f}%")
    print()

print(f"広告ユニットエコノミクス成立率(LTV_reader×0.7 > 1.3×CPA_reader): {viable.mean()*100:.1f}%")
print(f"読者1人あたりLTV 中央値: {np.percentile(ltv_reader,50):,.0f}円 / 広告CPA中央値: {np.percentile(cpr,50):,.0f}円")
