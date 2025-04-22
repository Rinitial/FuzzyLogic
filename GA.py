import random
import math

pop_size = 20
gen_max = 10
batas_bawah = -10
batas_atas = 10
peluang_c = 0.8
peluang_m = 0.1
dimensi = 2

#inisialisasi populasi secara acak dengan representasi nilai float
#dengan setiap individu akan di insert ke dalam list kosong
def inisialisasi_pop():
    populasi = [None] * pop_size
    for i in range(pop_size):
        individu = [0] * dimensi
        for j in range(dimensi):
            nilai = random.uniform(batas_bawah, batas_atas)#inisialisasi nilai acak dengan rentang batas atas dan batas bawah
            individu[j] = nilai
        populasi[i] = individu#proses penyimpanan individu ke dalam populasi
    return populasi

#menghitung fungsi objektif dengan menggunakan rumus yang diberikan
def fungsi_objectif(x):
    x1 = x[0]
    x2 = x[1]

    try:
        bagian1 = math.sin(x1) * math.cos(x2) * math.tan(x1+x2)
        bagian2 = 3/4 * math.exp(1 - math.sqrt(x1**2))
        return -(bagian1 + bagian2)# berfugsi untuk meminimalkan fungsi
    except:
        return float('inf')#solusi jika terjadi kasu tidak terdefinisi
    
#Evaluasi populasi berdasarkan dari nilai fitness tiap individu
#Mengembalikan daftar nilai fitness
def evaluasi_populasi(populasi):
    hasil = []
    for individu in populasi:
        nilai = fungsi_objectif(individu)
        hasil.append(nilai)
    return hasil
#function yang berfungsi untuk mengubah nilai decimal ke dalam biner
#function ini berguna untuk membantu proses decode nilai real kedalam biner
def ubahIntKeBiner(n):
    biner = ['0'] * 16#representasi dari 16 bit biner
    for i in range(15, -1, -1):
        if n >= 2 ** i:
            biner[15-i] = '1'
            n -= 2**i
    return ''.join(biner)
#decode individu menjadi kromosom biner
def decode(individu):
    biner = [0.0] * len(individu)
    for i in range(len(individu)):
        nilai_real = individu[i]
        #proses merubah nilai real ke biner dengan menggunakan bantuan funstion ubahIntKeBiner
        nilai_int = int( (nilai_real - batas_bawah) / (batas_atas - batas_bawah) * (2 ** 16 - 1))
        biner[i] = ubahIntKeBiner(nilai_int)
    return biner
#Pemilihan orang tua menggunakan tournament selection
def tournamentSelection(populasi, fitness, n = 3):
    pilihan = []
    for _ in range(len(populasi)):
        kandidat = random.sample(list(zip(populasi, fitness)), n)#Memilih kandidat secara acak sebanyak n
        Kan_terpilih = min(kandidat, key = lambda x: x[1])#memilih fitness terbaik dari n kandidat yang sudah di pilih
        pilihan.append(Kan_terpilih[0])#proses penyimpanan individu
    return pilihan
#Function crossover untuk menghasil kan child dari parent yang telah di pilih
def crossover(p1,p2):
    if random.random() < peluang_c:
        nilai = random.random()
        c1 = []
        c2 = []
        #proses crossover pada setiap dimensi
        for i in range(dimensi):
            hasil1 = nilai * p1[i] + (1 - nilai) * p2[i]
            hasil2 = nilai * p2[i] + (1 - nilai) * p1[i]

            c1.append(hasil1)
            c2.append(hasil2)
        #proses pembatasan hasil dari crossover agar tetap valid
        for i in range(dimensi):
            c1[i] = max(min(c1[i],batas_atas),batas_bawah)
            c2[i] = max(min(c2[i],batas_atas),batas_bawah)

        return c1,c2#child dari proses crossover
    else:
        return p1[:],p2[:]#proses pengembalian orang tua jika tidak terjadi crossover
    
#Function mutasi yang berfungsi untuk mengubah nilai secara acak dalam individu
def mutasi(individu):
    i=0
    while i < dimensi:
        probabilitas = random.random()
        if probabilitas < peluang_m:
            nilai = random.uniform(-1, 1)
            nilaiMutasi = individu[i] + nilai#mengubah nilai dari individu
            #Membatasi agar nilai tetap valid
            if nilaiMutasi > batas_atas:
                nilaiMutasi = batas_atas
            elif nilaiMutasi < batas_bawah:
                nilaiMutasi = batas_bawah
            individu[i] = nilaiMutasi
        i +=1
    return individu
#function utama yang berfungsi untuk menjalankan algoritma genetika sebagai mana mestinya
def generasi_GA():
    print("Algoritma dimulai....")
    populasi = inisialisasi_pop()#proses inisialisasi populasi
    solusi_terbaik = None
    fitness_terbaik = float('inf')
    riwayat_fitness = []#variabel tempat untuk menyimpan fitness terbaik
    kromosom_biner = None

    for i in range(gen_max):
        nilai_fitness = evaluasi_populasi(populasi)#Proses evaluasi fitness
        #Proses pencarian individu dengan nilai fitness terbaik (proses elitisme)
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
        #Proses pembaharuan apabila ditemukannya individu yang lebih baik
        if elite_fitness < fitness_terbaik:
            fitness_terbaik = elite_fitness
            solusi_terbaik = [0.0] * dimensi
            for k in range(dimensi):
                solusi_terbaik[k] = elite[k]
            kromosom_biner = decode(solusi_terbaik)
        riwayat_fitness.append(fitness_terbaik)#Menyimpan fitness terbaik ke dalam list
        print(f"Individu pada Generasi {i + 1}:")
        for j in range(len(populasi)):
            print(f"Individu {j + 1}: {populasi[j]}, Fitness: {nilai_fitness[j]}")
        print(f"Fitness Terbaik = {fitness_terbaik}, Fungsi = {fungsi_objectif(solusi_terbaik)}")
        print("")
        #Pemilihan orang tua dan crossover
        parent = tournamentSelection(populasi,nilai_fitness)
        #Pembuatan populasi baru
        generasi = [None] * pop_size
        idx = 0
        for j in range(0,pop_size - 1, 2):
            p1 = parent[j]
            p2 = parent[j+1]
            c1,c2 = crossover(p1,p2)# proses crossover
            c1 = mutasi(c1)#muatasi pada child pertama
            c2 = mutasi(c2)#mutasi pada child ke 2
            generasi[idx] = c1
            generasi[idx + 1] = c2
            idx += 2
        generasi[pop_size-1] = elite#Mempertahankan individu terbaik
        populasi = generasi#Pembaharuan populasi
    return solusi_terbaik,fitness_terbaik,riwayat_fitness,kromosom_biner
#Run GA
hasil, fitness, riwayat, kromosom_biner= generasi_GA()

#Tampilan untuk hasil akhir
print("\nKromosom Terbaik:", ''.join(kromosom_biner))
print(f"Dimensi 1 = {hasil[0]}")
print(f"Dimensi 2 = {hasil[1]}")
print(f"Fitness = {fitness}")
print(f"Nilai Fungsi = {fungsi_objectif(hasil)}")
