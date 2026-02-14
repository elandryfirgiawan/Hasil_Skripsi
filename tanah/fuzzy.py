import numpy as np
import skfuzzy as fuzz

def kualitas_tanah_fuzzy(pH, KTK, Corg, N, P, K):

    # ======================================================
    # 1️⃣ FUZZIFIKASI
    # ======================================================

    # ===== pH =====
    x_pH = np.linspace(0, 14, 100)
    pH_masam  = fuzz.trimf(x_pH, [0, 0, 6])
    pH_netral = fuzz.trimf(x_pH, [5, 7, 9])
    pH_basa   = fuzz.trimf(x_pH, [8, 14, 14])

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


    # ===== C-Organik =====
    x_C = np.linspace(0, 5, 100)
    C_r = fuzz.trimf(x_C, [0, 0, 1])
    C_s = fuzz.trimf(x_C, [0.8, 2, 3])
    C_t = fuzz.trimf(x_C, [2.5, 5, 5])

    μ_C = [
        fuzz.interp_membership(x_C, C_r, Corg),
        fuzz.interp_membership(x_C, C_s, Corg),
        fuzz.interp_membership(x_C, C_t, Corg)
    ]


    # ===== N Total =====
    x_N = np.linspace(0, 1, 100)
    N_r = fuzz.trimf(x_N, [0, 0, 0.2])
    N_s = fuzz.trimf(x_N, [0.15, 0.4, 0.6])
    N_t = fuzz.trimf(x_N, [0.5, 1, 1])

    μ_N = [
        fuzz.interp_membership(x_N, N_r, N),
        fuzz.interp_membership(x_N, N_s, N),
        fuzz.interp_membership(x_N, N_t, N)
    ]


    # ===== P Total =====
    x_P = np.linspace(0, 100, 100)
    P_r = fuzz.trimf(x_P, [0, 0, 25])
    P_s = fuzz.trimf(x_P, [20, 50, 70])
    P_t = fuzz.trimf(x_P, [60, 100, 100])

    μ_P = [
        fuzz.interp_membership(x_P, P_r, P),
        fuzz.interp_membership(x_P, P_s, P),
        fuzz.interp_membership(x_P, P_t, P)
    ]


    # ===== K Total =====
    x_K = np.linspace(0, 100, 100)
    K_r = fuzz.trimf(x_K, [0, 0, 25])
    K_s = fuzz.trimf(x_K, [20, 50, 70])
    K_t = fuzz.trimf(x_K, [60, 100, 100])

    μ_K = [
        fuzz.interp_membership(x_K, K_r, K),
        fuzz.interp_membership(x_K, K_s, K),
        fuzz.interp_membership(x_K, K_t, K)
    ]


    # ======================================================
    # 2️⃣ INFERENSI (MIN)
    # ======================================================

    rules = []

    # RULE 1 → Sehat (semua tinggi & pH netral)
    alpha_sehat = min(μ_pH[1], μ_KTK[2], μ_C[2], μ_N[2], μ_P[2], μ_K[2])
    rules.append((alpha_sehat, 2))

    # RULE 2 → Tidak Sehat (pH masam atau unsur rendah)
    alpha_tidak = max(
        min(μ_pH[0], μ_KTK[0]),
        μ_C[0],
        μ_N[0]
    )
    rules.append((alpha_tidak, 0))

    # RULE 3 → Kurang Sehat (kondisi sedang)
    alpha_kurang = min(μ_pH[1], μ_KTK[1])
    rules.append((alpha_kurang, 1))


    # ======================================================
    # 3️⃣ DEFUZZIFIKASI SUGENO (WEIGHTED AVERAGE)
    # ======================================================

    numerator = sum(w * z for w, z in rules)
    denominator = sum(w for w, z in rules)

    if denominator == 0:
        return 0

    hasil = numerator / denominator

    # ======================================================
    # 4️⃣ KLASIFIKASI AKHIR
    # ======================================================

    if hasil < 0.5:
        return 0      # Tidak Sehat
    elif hasil < 1.5:
        return 1      # Kurang Sehat
    else:
        return 2      # Sehat
