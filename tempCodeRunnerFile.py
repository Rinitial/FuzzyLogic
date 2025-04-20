import random
import math

pop_size = 50
gen_max = 100
batas_bawah = -10
batas_atas = 10
peluang_c = 0.8
peluang_m = 0.3
dimensi = 2
def inisialisasi_pop():
    populasi = [None] * pop_size
    for i in range(pop_size):
        individu = [0] * dimensi
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
            kromosom = encode(individu)
            individu_terdecode = decode(kromosom)

            nilai = fungsi_objectif(individu_terdecode)
            hasil += [nilai]
            i = i+ 1
        except IndexError:
            break
    return hasil

def ubahIntKeBiner(n):
    biner = ['0'] * 16
    for i in range(15, -1, -1):
        if n >= 2 ** i:
            biner[15-i] = '1'
            n -= 2**i
    return ''.join(biner)
def ubahBinerKeInt(biner):
    hasil = 0
    for i in range(16):
        if biner[i] == '1':
            hasil += 2 ** (15 - i)
    return hasil
def encode(individu):
    biner = [0.0] * len(individu)
    for i in range(len(individu)):
        nilai_real = individu[i]
        nilai_int = int( (nilai_real - batas_bawah) / (batas_atas - batas_bawah) * (2 ** 16 - 1))
        biner[i] = ubahIntKeBiner(nilai_int)
    return biner
def decode(biner):
    individu = [0.0] * len(biner)
    for i in range(len(biner)):
        nilai_int = ubahBinerKeInt(biner[i])
        nilai_real = batas_bawah + (nilai_int / (2 ** 16 - 1)) * (batas_atas - batas_bawah)
        individu[i] = nilai_real
    return individu
def tournamentSelection(populasi, fitness, n = 3):
    pilihan = []
    for _ in range(len(populasi)):
        kandidat = random.sample(list(zip(populasi, fitness)), n)
        Kan_terpilih = min(kandidat, key = lambda x: x[1])
        pilihan.append(Kan_terpilih[0])
    return pilihan
def crossover(p1,p2):
    if random.random() < peluang_c:
        nilai = random.random()
        c1 = []
        c2 = []
        for i in range(dimensi):
            hasil1 = nilai * p1[i] + (1 - nilai) * p2[i]
            hasil2 = nilai * p2[i] + (1 - nilai) * p1[i]

            c1.append(hasil1)
            c2.append(hasil2)

        for i in range(dimensi):
            c1[i] = max(min(c1[i],batas_atas),batas_bawah)
            c2[i] = max(min(c2[i],batas_atas),batas_bawah)

        return c1,c2
    else:
        return p1[:],p2[:]
    
def mutasi(individu):
    i=0
    while i < dimensi:
        probabilitas = random.random()
        if probabilitas < peluang_m:
            nilai = random.uniform(-1, 1)
            nilaiMutasi = individu[i] + nilai

            if nilaiMutasi > batas_atas:
                nilaiMutasi = batas_atas
            elif nilaiMutasi < batas_bawah:
                nilaiMutasi = batas_bawah
            individu[i] = nilaiMutasi
        i +=1
    return individu
def GA():
    print("Algoritma dimulai....")
    populasi = inisialisasi_pop()
    solusi_terbaik = None
    fitness_terbaik = float('inf')
    riwayat_fitness = []

    for i in range(gen_max):
        print("generasi", i+1, "dimulai...")

        nilai_fitness = evaluasi_populasi(populasi)

        fitness_trkcl = nilai_fitness[0]
        index = 0
        for j in range(1, len(nilai_fitness)):
            if nilai_fitness[j] < fitness_trkcl:
                fitness_trkcl = nilai_fitness[j]
                index = j
        elite = [0.0] * dimensi
        for k in range(dimensi):
            elite[k] = populasi[index][k]
        elite_fitness = nilai_fitness[index]

        if elite_fitness < fitness_terbaik:
            fitness_terbaik = elite_fitness
            solusi_terbaik = [0.0] * dimensi
            for k in range(dimensi):
                solusi_terbaik[k] = elite[k]
        riwayat_fitness.append(fitness_terbaik)

        parent = tournamentSelection(populasi,nilai_fitness)

        generasi = [None] * pop_size
        idx = 0
        for j in range(0,pop_size - 1, 2):
            p1 = parent[j]
            p2 = parent[j+1]
            c1,c2 = crossover(p1,p2)
            c1 = mutasi(c1)
            c2 = mutasi(c2)
            generasi[idx] = c1
            generasi[idx + 1] = c2
            idx += 2

        generasi[pop_size-1] = elite

        populasi = generasi

        print("Generasi", i+1, "| Fitness Terbaik: ", fitness_terbaik,"| Solusi: ", solusi_terbaik)

    return solusi_terbaik,fitness_terbaik,riwayat_fitness
hasil, fitness, riwayat = GA()

kromosom_terbaik = encode(hasil)
print("\nKromosom Terbaik:", ''.join(kromosom_terbaik))
d1 = hasil[0]
d2 = hasil[1]
print(f"Dimensi 1 = {d1}")
print(f"Dimensi 2 = {d2}")
print(f"Fitness = {fitness}")
print(f"Nilai Fungsi = {fungsi_objectif(hasil)}")
