from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .fuzzy import kualitas_tanah_fuzzy

def form_input(request):
    if request.method == 'POST':
        pH = float(request.POST['pH'])
        KTK = float(request.POST['KTK'])
        Corg = float(request.POST['C_Organik'])
        N = float(request.POST['N_Total'])
        P = float(request.POST['P_Total'])
        K = float(request.POST['K_Total'])

        hasil = kualitas_tanah_fuzzy(pH, KTK, Corg, N, P, K)

        label = {
            0: "Tidak Sehat",
            1: "Kurang Sehat",
            2: "Sehat"
        }

        return render(request, 'tanah/result.html', {
            'hasil': hasil,
            'label': label[hasil]
        })

    return render(request, 'tanah/form.html')
