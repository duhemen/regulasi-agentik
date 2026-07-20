import streamlit as st
import autogen
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(page_title="Asisten Agen Regulasi AI", page_icon="⚖️", layout="wide")
st.title("⚖️ LegalAI-Agent: Analis Regulasi & Kepatuhan AI")
st.caption("Sistem Multi-Agent Lokal + RAG Dinamis (Bertenaga Qwen 2.5 7B & DeepSeek-R1 8B)")

DB_DIR = "./chroma_db"

# Fungsi memuat Embedding Model (Dicache agar hemat RAM)
@st.cache_resource
def ambil_model_embedding():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={'device': 'cpu'} # Sangat ringan di i9 Gen 13
    )

embedding_model = ambil_model_embedding()

# ==========================================
# 2. PANEL SAMPING (SIDEBAR): UNTUK UPDATE REGULASI
# ==========================================
with st.sidebar:
    st.header("📂 Pembaruan Regulasi Dinamis")
    st.write("Ada undang-undang atau revisi baru? Unggah langsung di sini untuk memperbarui otak AI.")
    
    # Komponen Unggah File PDF
    uploaded_files = st.file_uploader(
        "Pilih berkas PDF Regulasi Baru:", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    tombol_proses = st.button("🚀 Ingest & Perbarui Database RAG", use_container_width=True)
    
    if tombol_proses and uploaded_files:
        with st.spinner("⏳ Sedang mengekstrak dan mengindeks dokumen baru..."):
            try:
                all_docs = []
                # Buat folder temporer untuk membaca PDF
                os.makedirs("temp_pdf", exist_ok=True)
                
                for file_pdf in uploaded_files:
                    path_target = os.path.join("temp_pdf", file_pdf.name)
                    with open(path_target, "wb") as f:
                        f.write(file_pdf.getbuffer())
                    
                    # Baca PDF menggunakan LangChain
                    loader = PyPDFLoader(path_target)
                    all_docs.extend(loader.load())
                    
                    # Hapus file temp setelah dibaca
                    os.remove(path_target)
                
                # Potong teks hukum secara presisi
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
                potongan_dokumen = text_splitter.split_documents(all_docs)
                
                # Masukkan/Tambahkan (Upsert) ke ChromaDB lokal tanpa menghapus data lama
                db_vektor = Chroma.from_documents(
                    documents=potongan_dokumen,
                    embedding=embedding_model,
                    persist_directory=DB_DIR
                )
                
                st.success(f"🎉 Sukses! {len(potongan_dokumen)} pasal baru berhasil disuntikkan ke database lokal!")
                st.rerun() # Refresh aplikasi agar data baru langsung bisa dicari
            except Exception as e:
                st.error(f"Gagal memproses dokumen: {str(e)}")
    elif tombol_proses and not uploaded_files:
        st.warning("Silakan pilih minimal satu file PDF terlebih dahulu, Emen!")

# ==========================================
# 3. KONEKSI KE DATA RETRIEVER
# ==========================================
def dapatkan_retriever():
    if os.path.exists(DB_DIR):
        db_lokal = Chroma(persist_directory=DB_DIR, embedding_function=embedding_model)
        return db_lokal.as_retriever(search_kwargs={"k": 3})
    return None

pencari_pasal = dapatkan_retriever()

# ==========================================
# 4. KANTONG RIWAYAT CHAT & ANTARMUKA
# ==========================================
if "riwayat_pesan" not in st.session_state:
    st.session_state.riwayat_pesan = []

# Tampilkan chat lama di layar utama
for chat in st.session_state.riwayat_pesan:
    with st.chat_message(chat["peran"]):
        st.markdown(chat["konten"])

# ==========================================
# 5. FUNGSI LOGIKA MULTI-AGENT AUTOGEN
# ==========================================
def jalankan_analisis_agen(pertanyaan, konteks):
    config_qwen = [{"model": "qwen2.5:7b-instruct", "api_type": "openai", "api_key": "NULL", "base_url": "http://localhost:11434/v1"}]
    config_deepseek = [{"model": "deepseek-r1:8b", "api_type": "openai", "api_key": "NULL", "base_url": "http://localhost:11434/v1"}]

    # Agen 1: Analis Hukum (Berbasis Qwen 7B)
    analis_hukum = autogen.AssistantAgent(
        name="Analis_Hukum",
        llm_config={"config_list": config_qwen, "temperature": 0.0},
        system_message=f"Anda Ahli Hukum AI Senior Indonesia. Tugas Anda membedah kasus secara objektif dengan pasal resmi ini:\n---\n{konteks}\n---\nSebutkan nama regulasinya dengan sangat jelas."
    )

    # Agen 2: Pengecek Kepatuhan & Risiko Sanksi (Berbasis DeepSeek-R1 8B)
    pengecek_kepatuhan = autogen.AssistantAgent(
        name="Pengecek_Kepatuhan",
        llm_config={"config_list": config_deepseek, "temperature": 0.0},
        system_message="Anda Auditor Risiko dan Sanksi Hukum AI. Tugas Anda menganalisis paparan dari Analis_Hukum. Cari potensi pelanggaran etika digital, sanksi administrasi, denda materiil, hingga pemutusan akses (blokir) berdasarkan dokumen terkait. Berikan kesimpulan akhir yang rapi dan terstruktur untuk pengguna."
    )

    # Agen Jembatan Pengguna (User Proxy)
    user_proxy = autogen.UserProxyAgent(
        name="Emen_Proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False
    )

    # 🛠️ PENYEMPURNAAN ALUR: Mengunci urutan bicara kaku agar semua kebagian peran secara adil
    urutan_bicara = [user_proxy, analis_hukum, pengecek_kepatuhan]

    grup_chat = autogen.GroupChat(
        agents=[user_proxy, analis_hukum, pengecek_kepatuhan], 
        messages=[], 
        max_round=4, # Dinaikkan menjadi 4 ronde agar alur lengkap (User -> Qwen -> DeepSeek -> Selesai)
        speaker_selection_method="round_robin", # Paksa alur berurutan sesuai daftar
        allow_repeat_speaker=False # Melarang agen berbicara dua kali berturut-turut
    )
    
    # Pengelola Grup Chat (LLM sengaja di-None-kan untuk menghemat RAM laptop Emen)
    pengelola = autogen.GroupChatManager(groupchat=grup_chat, llm_config=None)
    
    # Memulai debat agen digital
    user_proxy.initiate_chat(pengelola, message=pertanyaan)
    
    # Menyisir dari pesan paling akhir untuk mengamankan jawaban yang tidak kosong
    for msg in reversed(grup_chat.messages):
        if msg.get('content') and msg['content'].strip():
            return msg['content']
            
    return "⚠️ Maaf, tim agen menyelesaikan diskusi tanpa mengeluarkan draf jawaban."

# ==========================================
# 6. INPUT CHAT PENGGUNA
# ==========================================
if input_user := st.chat_input("Tanyakan kepatuhan hukum terkait AI di sini..."):
    with st.chat_message("user"):
        st.markdown(input_user)
    st.session_state.riwayat_pesan.append({"peran": "user", "konten": input_user})

    with st.chat_message("assistant"):
        if pencari_pasal is None:
            st.error("⚠️ Database RAG masih kosong! Silakan unggah dokumen regulasi pertama kamu di panel samping kiri terlebih dahulu.")
        else:
            with st.spinner("🕵️ Tim Agen AI sedang berdiskusi membedah pasal regulasi..."):
                try:
                    # RAG mencari pasal relevan
                    hasil_cari = pencari_pasal.invoke(input_user)
                    konteks_teks = "\n\n".join([doc.page_content for doc in hasil_cari])
                    
                    # AutoGen mengeksekusi analisis kolaboratif
                    jawaban_final = jalankan_analisis_agen(input_user, konteks_teks)
                    
                    st.markdown(jawaban_final)
                    st.session_state.riwayat_pesan.append({"peran": "assistant", "konten": jawaban_final})
                except Exception as e:
                    st.error(f"Terjadi kendala teknis: {str(e)}")
