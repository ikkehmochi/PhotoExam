from sentence_transformers import SentenceTransformer, util

def st_grader(text1, text2):
    model=SentenceTransformer("output2/100epochs_finetune_indoessay_distiluse-base-multilingual-cased-v2-2023-12-10_16-38-46")
    encoded_text1=model.encode(text1)
    encoded_text2=model.encode(text2)
    similarity=util.cos_sim(encoded_text1, encoded_text2)
    sim_score=similarity[0][0]
    if sim_score>0.8:
        return 1
    else:
        return 0

if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    result = st_grader("Badan Penyelidik Usaha Persiapan Kemerdekaan Indonesia (BPUPKI) adalah badan yang dibentuk pada tahun 1945 oleh pemerintah pendudukan Jepang di Indonesia selama masa Perang Dunia II. Badan ini bertugas untuk menyelidiki dan merancang rencana kemerdekaan Indonesia setelah Jepang menyerah kepada Sekutu. BPUPKI terdiri dari berbagai pemimpin politik, tokoh masyarakat, dan tokoh agama dari berbagai latar belakang etnis di Indonesia. Salah satu tugas utamanya adalah merumuskan dasar negara dan konstitusi yang akan membentuk dasar bagi negara Indonesia merdeka. Hasil utama dari rapat-rapat BPUPKI adalah pembentukan Pancasila sebagai dasar negara Indonesia dan penyusunan UUD 1945, yang hingga kini menjadi konstitusi Indonesia. Setelah merumuskan dasar negara dan konstitusi, BPUPKI kemudian berkembang menjadi Panitia Persiapan Kemerdekaan Indonesia (PPKI) yang mengambil peran lebih lanjut dalam proses kemerdekaan Indonesia hingga proklamasi kemerdekaan pada tanggal 17 Agustus 1945.", "Panitia Persiapan Kemerdekaan Indonesia (PPKI) adalah lembaga yang dibentuk pada bulan Agustus 1945 untuk mempersiapkan proklamasi kemerdekaan Indonesia. PPKI terbentuk setelah Badan Penyelidik Usaha Persiapan Kemerdekaan Indonesia (BPUPKI) mengadakan sidangnya yang terakhir pada 18 Agustus 1945.PPKI terdiri dari tokoh-tokoh nasional Indonesia, termasuk pemimpin politik, tokoh agama, dan tokoh masyarakat dari berbagai daerah di Indonesia. Tugas utama PPKI adalah mengesahkan naskah proklamasi kemerdekaan Indonesia yang telah disiapkan oleh Soekarno dan Mohammad Hatta. Pada 17 Agustus 1945, PPKI secara resmi mengesahkan naskah proklamasi dan memutuskan untuk menyatakan kemerdekaan Indonesia.Selain itu, PPKI juga mengambil peran penting dalam menetapkan konstitusi sementara dan membentuk pemerintahan awal Indonesia. PPKI berperan dalam menjalankan proses awal negara Indonesia pasca-proklamasi kemerdekaan, menegaskan kedaulatan Indonesia, serta membentuk landasan politik dan administratif bagi negara yang baru merdeka.")
    print(result)
