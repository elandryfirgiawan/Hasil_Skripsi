# ============================================================
# FUNGSI KEANGGOTAAN
# ============================================================

# ---------------- pH ----------------
def mu_ph_masam(x):
    if x <= 0: return 1
    elif 0 < x < 6: return (6-x)/6
    else: return 0

def mu_ph_netral(x):
    if x <= 5: return 0
    elif 5 < x < 7: return (x-5)/2
    elif 7 <= x < 9: return (9-x)/2
    else: return 0

def mu_ph_basa(x):
    if x <= 8: return 0
    elif 8 < x < 14: return (x-8)/6
    else: return 1

# ---------------- KTK ----------------
def mu_ktk_rendah(x):
    if x <= 5: return 1
    elif 5 < x < 17: return (17-x)/12
    else: return 0

def mu_ktk_sedang(x):
    if x <= 16: return 0
    elif 16 < x < 20: return (x-16)/4
    elif 20 <= x < 25: return (25-x)/5
    else: return 0

def mu_ktk_tinggi(x):
    if x <= 24: return 0
    elif 24 < x < 40: return (x-24)/16
    else: return 1

# ---------------- C-Organik ----------------
def mu_c_rendah(x):
    if x <= 1: return 1
    elif 1 < x < 2.5: return (2.5-x)/1.5
    else: return 0

def mu_c_sedang(x):
    if x <= 2: return 0
    elif 2 < x < 3: return (x-2)
    elif 3 <= x < 4: return (4-x)
    else: return 0

def mu_c_tinggi(x):
    if x <= 3.5: return 0
    elif 3.5 < x < 5: return (x-3.5)/1.5
    else: return 1

# ---------------- N Total ----------------
def mu_n_rendah(x):
    if x <= 0.10: return 1
    elif 0.10 < x < 0.13: return (0.13-x)/0.03
    else: return 0

def mu_n_sedang(x):
    if x <= 0.12: return 0
    elif 0.12 < x < 0.16: return (x-0.12)/0.04
    elif 0.16 <= x < 0.20: return (0.20-x)/0.04
    else: return 0

def mu_n_tinggi(x):
    if x <= 0.19: return 0
    elif 0.19 < x < 0.25: return (x-0.19)/0.06
    else: return 1

# ---------------- P Total ----------------
def mu_p_rendah(x):
    if x <= 10: return 1
    elif 10 < x < 21: return (21-x)/11
    else: return 0

def mu_p_sedang(x):
    if x <= 20: return 0
    elif 20 < x < 30: return (x-20)/10
    elif 30 <= x < 41: return (41-x)/11
    else: return 0

def mu_p_tinggi(x):
    if x <= 40: return 0
    elif 40 < x < 100: return (x-40)/60
    else: return 1

# ---------------- K Total ----------------
def mu_k_rendah(x):
    if x <= 100: return 1
    elif 100 < x < 155: return (155-x)/55
    else: return 0

def mu_k_sedang(x):
    if x <= 150: return 0
    elif 150 < x < 200: return (x-150)/50
    elif 200 <= x < 255: return (255-x)/55
    else: return 0

def mu_k_tinggi(x):
    if x <= 250: return 0
    elif 250 < x < 500: return (x-250)/250
    else: return 1


# ============================================================
# SISTEM FUZZY SUGENO 
# ============================================================

def kualitas_tanah_fuzzy(pH, KTK, Corg, N, P, K):

    μ_pH = [mu_ph_masam(pH), mu_ph_netral(pH), mu_ph_basa(pH)]
    μ_KTK = [mu_ktk_rendah(KTK), mu_ktk_sedang(KTK), mu_ktk_tinggi(KTK)]
    μ_C = [mu_c_rendah(Corg), mu_c_sedang(Corg), mu_c_tinggi(Corg)]
    μ_N = [mu_n_rendah(N), mu_n_sedang(N), mu_n_tinggi(N)]
    μ_P = [mu_p_rendah(P), mu_p_sedang(P), mu_p_tinggi(P)]
    μ_K = [mu_k_rendah(K), mu_k_sedang(K), mu_k_tinggi(K)]

    pH_labels = ["Asam", "Netral", "Basa"]
    other_labels = ["Rendah", "Sedang", "Tinggi"]

    def get_dominant(values, labels):
        idx = values.index(max(values))
        return labels[idx], values[idx]

    pH_label, pH_val = get_dominant(μ_pH, pH_labels)
    KTK_label, KTK_val = get_dominant(μ_KTK, other_labels)
    C_label, C_val = get_dominant(μ_C, other_labels)
    N_label, N_val = get_dominant(μ_N, other_labels)
    P_label, P_val = get_dominant(μ_P, other_labels)
    K_label, K_val = get_dominant(μ_K, other_labels)

    # Rule 
    if (pH_label=="Netral" and KTK_label=="Tinggi" and
        C_label=="Tinggi" and N_label=="Tinggi" and
        P_label=="Tinggi" and K_label=="Tinggi"):
        z_rule = 2
    elif (pH_label=="Asam" or C_label=="Rendah" or N_label=="Rendah"):
        z_rule = 0
    else:
        z_rule = 1

    alpha_predikat = min(pH_val, KTK_val, C_val, N_val, P_val, K_val)

    if alpha_predikat != 0:
        z_defuzz = (alpha_predikat * z_rule) / alpha_predikat
    else:
        z_defuzz = 0

    if z_defuzz >= 1.5:
        return 2
    elif z_defuzz <= 0.5:
        return 0
    else:
        return 1