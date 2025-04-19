import random
import math

pop_size = 50
gen_max = 100
batas_bawah = -10
batas_atas = 10
peluang_c = 0.8
peluaamg_m = 0.1
dimensi = 2

def inisialisasi_pop():
    populasi = [] * pop_size
    for i in range(pop_size):
        individu = [0] * 2
        for j in range(dimensi):
            nilai = random.uniform(batas_bawah, batas_atas)
            individu[j] = nilai
    populasi[i] = individu
    return populasi

def fungsi_objectif(x):
    x1 = x[0]
    x2 = x[1]

    try:
        bagian1 = math.sin(x1) * math.cos(x2) * math.tan(x1+x2)
        bagian2 = 3/4 * math.exp(1 - math.sqrt(x1**2))
        return -(bagian1 + bagian2)
    except:
        return float('inf')
    
def evaluasi_populasi(populasi):
    hasil = []
    i = 0
    while True:
        try:
            individu = populasi[i]
            x1 = individu[0]
            x2 = individu[1]
            nilai = fungsi_objectif(x1,x2)
            hasil += [nilai]
            i = i+ 1
        except IndexError:
            break
    return hasil