import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def main():
    print("==================================================")
    print("🚀 MEMULAI PROSES INGESTI DOKUMEN REGULASI AI EMEN")
    print("==================================================")

    # 1. Daftar 5 file PDF milik Emen yang wajib ada di folder yang sama
    pdf_files = [
        "CoE_et_AI_GBR.pdf",
        "SE_MENKOMINFO_No_9_Tahun_2023.pdf",
        "SKB_Pedoman_Pemanfaatan_Kecerdasan_Artisial_2026.pdf",
        "UU_Nomor_1_Tahun_2024.pdf",
        "UU_Nomor_27_Tahun_2022.pdf"
    ]

    all_docs = []
    
    # 2. Membaca dan mengekstrak teks dari setiap PDF
    for pdf in pdf_files:
        if os.path.exists(pdf):
            print(f"📖 Membaca file: {pdf} ...")
            loader = PyPDFLoader(pdf)
            all_docs.extend(loader.load())
        else:
            print(f"❌ Eror: File {pdf} tidak ditemukan! Pastikan file ada di folder C:\\regulasi-agentik")
            return

    print(f"\n✅ Berhasil memuat total {len(all_docs)} halaman dari seluruh PDF.")

    # 3. Memotong teks hukum menjadi bagian kecil (chunks)
    # Aturan hukum harus dipotong presisi agar pasal tidak terputus di tengah kalimat
    print("✂️ Memotong teks menjadi potongan pasal yang presisi...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=150,
        length_function=len
    )
    docs = text_splitter.split_documents(all_docs)
    print(f"🧩 Menghasilkan {len(docs)} potongan teks kecil siap indeks.")

    # 4. Inisialisasi Model Embedding Lokal (Multilingual)
    # Menggunakan model serba guna yang sangat fasih memetakan konteks Indonesia-Inggris
    print("\n🧠 Mengunduh & memuat model embedding lokal (bge-m3)...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={'device': 'cpu'} # Berjalan super ringan di Core i9 kamu
    )

    # 5. Membuat dan menyimpan Database Vektor ke dalam harddisk laptop
    persist_directory = "./chroma_db"
    print(f"💾 Menyimpan data vektor ke folder lokal: {persist_directory} ...")
    
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    print("\n==================================================")
    print("🎉 SUKSES! Database RAG lokal Emen siap digunakan!")
    print("==================================================")

if __name__ == "__main__":
    main()
