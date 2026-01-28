import numpy as np
import skfuzzy as fuzz

def kualitas_tanah_fuzzy(pH, KTK, Corg, N, P, K):
    # ===== pH =====
    x_pH = np.linspace(0, 14, 100)
    pH_masam = fuzz.trimf(x_pH, [0, 0, 6])
    pH_netral = fuzz.trimf(x_pH, [5, 7, 9])
    pH_basa = fuzz.trimf(x_pH, [8, 14, 14])

    μ_pH = [
        fuzz.interp_membership(x_pH, pH_masam, pH),
        fuzz.interp_membership(x_pH, pH_netral, pH),
        fuzz.interp_membership(x_pH, pH_basa, pH)
    ]

    # ===== KTK =====
    x_KTK = np.linspace(5, 50, 100)
    KTK_r = fuzz.trimf(x_KTK, [5, 5, 17])
    KTK_s = fuzz.trimf(x_KTK, [16, 25, 35])
    KTK_t = fuzz.trimf(x_KTK, [30, 50, 50])

    μ_KTK = [
        fuzz.interp_membership(x_KTK, KTK_r, KTK),
        fuzz.interp_membership(x_KTK, KTK_s, KTK),
        fuzz.interp_membership(x_KTK, KTK_t, KTK)
    ]

    # ===== Nilai Output Sugeno =====
    # 0 = Tidak Sehat, 1 = Kurang Sehat, 2 = Sehat
    rules = [
        (min(μ_pH[0], μ_KTK[0]), 0),
        (min(μ_pH[1], μ_KTK[1]), 1),
        (min(μ_pH[2], μ_KTK[2]), 2),
    ]

    numerator = sum(w * z for w, z in rules)
    denominator = sum(w for w, z in rules)

    if denominator == 0:
        return 0

    hasil = numerator / denominator

    if hasil < 0.5:
        return 0
    elif hasil < 1.5:
        return 1
    else:
        return 2
