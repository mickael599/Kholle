import hashlib
import io
import os
import re
from pathlib import Path
from PIL import Image, ImageOps
import streamlit as st
from google import genai
from google.genai import types

# ==============================================================================
# 1. CONFIGURATION DE LA PAGE & DESIGN 3D HYPER-IMMERSIPH
# ==============================================================================
st.set_page_config(
    page_title="Khôlle MPSI - Tuteur Socratique",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── FOND GLOBAL DE L'APPLICATION (Deep Cosmos Indigo) ── */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at 50% 12%, #1e1b4b 0%, #0b0f19 45%, #050811 100%) !important;
        background-attachment: fixed !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 820px !important;
    }

    /* ── BARRE LATÉRALE GLASSMORPHISM ── */
    [data-testid="stSidebar"] {
        background: rgba(11, 15, 25, 0.96) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.25) !important;
        backdrop-filter: blur(14px) !important;
    }

    /* ── CARTE HERO 3D FLOTTANTE ── */
    .hero-3d-box {
        perspective: 1200px;
        margin-bottom: 1.6rem;
    }

    .hero-3d-card {
        background: linear-gradient(135deg, rgba(30, 41, 69, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 24px;
        padding: 2rem 1.6rem;
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 35px 2px rgba(99, 102, 241, 0.28);
        backdrop-filter: blur(16px);
        transform-style: preserve-3d;
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .hero-3d-card:hover {
        transform: translateY(-6px) rotateX(2deg) scale(1.01);
        box-shadow: 0 32px 65px -15px rgba(0, 0, 0, 0.9), 0 0 45px 6px rgba(99, 102, 241, 0.4);
    }

    .hero-3d-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        padding: 6px 18px;
        border-radius: 9999px;
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.5);
    }

    .hero-3d-title {
        color: #ffffff !important;
        font-size: clamp(1.5rem, 4.5vw, 2.3rem) !important;
        font-weight: 800 !important;
        margin: 0 0 0.5rem 0 !important;
        letter-spacing: -0.03em !important;
        text-shadow: 0 3px 14px rgba(0,0,0,0.6);
    }

    .hero-3d-subtitle {
        color: #94a3b8 !important;
        font-size: clamp(0.88rem, 2.4vw, 1.02rem) !important;
        margin: 0 0 1.2rem 0 !important;
        line-height: 1.5;
    }

    .hero-status-pills {
        display: flex;
        gap: 8px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .hero-pill {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 5px 15px;
        font-size: 0.78rem;
        color: #cbd5e1;
        font-weight: 600;
        backdrop-filter: blur(8px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    /* ── BULLES DE CHAT 3D AVEC RELIEF ── */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(26, 34, 56, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 20px !important;
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.12) !important;
        margin-bottom: 1.1rem !important;
        backdrop-filter: blur(10px) !important;
        transition: transform 0.25s ease !important;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.7), 0 0 25px rgba(99, 102, 241, 0.22) !important;
    }

    /* ── BOUTONS 3D PHYSIQUES AVEC RELIEF ET PRESSION ── */
    div.stButton > button {
        background: linear-gradient(180deg, #312e81 0%, #1e1b4b 100%) !important;
        color: #ffffff !important;
        border: 1px solid #4f46e5 !important;
        border-bottom: 4px solid #3730a3 !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4), 0 0 18px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(180deg, #3730a3 0%, #312e81 100%) !important;
        border-color: #6366f1 !important;
        border-bottom: 4px solid #4338ca !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 24px rgba(79, 70, 229, 0.45) !important;
    }

    div.stButton > button:active {
        transform: translateY(3px) !important;
        border-bottom: 1px solid #4338ca !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6) !important;
    }

    /* ── RENDU MATHÉMATIQUE KATEX HAUTE DÉFINITION ── */
    .katex {
        font-size: 1.1em !important;
        color: #f8fafc !important;
    }

    .katex-display {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-left: 4px solid #6366f1 !important;
        border-radius: 14px !important;
        padding: 0.8em 1.3em !important;
        margin: 0.9em 0 !important;
        overflow-x: auto !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
    }

    /* ── ONGLETS 3D HAUTE DÉFINITION ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        padding: 8px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 9px 20px !important;
        color: #94a3b8 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45) !important;
    }

    /* ── ZONE DE SAISIE DE CHAT EN BAS ── */
    [data-testid="stChatInput"] {
        border-radius: 18px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        background: rgba(15, 23, 42, 0.9) !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(12px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. NETTOYEUR LATEX ROBUSTE (Zéro crochet, 100% KaTeX pur)
# ==============================================================================
def sanitize_latex(text: str) -> str:
    r"""
    Convertit automatiquement \[ ... \] en $$ ... $$ et \( ... \) en $ ... $.
    Nettoie les crochets bruts pour un affichage KaTeX mathématique impeccable.
    """
    if not text:
        return text
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
    return text

# ==============================================================================
# 3. GESTION PERSISTANTE SÉCURISÉE DE LA CLÉ API & MOT DE PASSE ADMIN
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
KEY_FILE_PATH = BASE_DIR / "CLE_API.txt"
SECRETS_FILE_PATH = BASE_DIR / ".streamlit" / "secrets.toml"
PASSWORD_HASH_PATH = BASE_DIR / "ADMIN_PASSWORD.hash"

def get_persisted_key() -> str:
    """Charge la clé API depuis secrets.toml, CLE_API.txt ou variable d'environnement."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key

    if KEY_FILE_PATH.exists():
        try:
            content = KEY_FILE_PATH.read_text(encoding="utf-8").strip()
            lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
            if lines:
                return lines[0]
        except Exception:
            pass

    try:
        sec = st.secrets.get("GEMINI_API_KEY", "").strip()
        if sec:
            return sec
    except Exception:
        pass

    return ""

def set_persisted_key(new_key: str):
    """Enregistre définitivement la clé sur disque pour qu'elle ne bouge plus."""
    new_key = new_key.strip()
    if not new_key:
        return
    try:
        KEY_FILE_PATH.write_text(f"{new_key}\n", encoding="utf-8")
        SECRETS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SECRETS_FILE_PATH.write_text(f'GEMINI_API_KEY = "{new_key}"\n', encoding="utf-8")
    except Exception as e:
        st.error(f"Erreur d'enregistrement : {e}")

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def get_admin_hash() -> str:
    if PASSWORD_HASH_PATH.exists():
        try:
            return PASSWORD_HASH_PATH.read_text(encoding="utf-8").strip()
        except Exception:
            return ""
    return ""

def set_admin_hash(pw: str):
    PASSWORD_HASH_PATH.write_text(hash_pw(pw), encoding="utf-8")

# ==============================================================================
# 4. ÉTAT DE SESSION
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_contents" not in st.session_state:
    st.session_state.api_contents = []

if "exercise_hash" not in st.session_state:
    st.session_state.exercise_hash = None

if "exercise_bytes" not in st.session_state:
    st.session_state.exercise_bytes = None

if "exercise_mime" not in st.session_state:
    st.session_state.exercise_mime = None

if "draft_hash" not in st.session_state:
    st.session_state.draft_hash = None

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

def reset_session():
    """Remet à zéro la séance de colle pour un nouvel exercice."""
    st.session_state.messages = []
    st.session_state.api_contents = []
    st.session_state.exercise_hash = None
    st.session_state.exercise_bytes = None
    st.session_state.exercise_mime = None
    st.session_state.draft_hash = None

# ==============================================================================
# 5. OPTIMISATION IMAGES SMARTPHONE (EXIF & COMPRESSION)
# ==============================================================================
def optimize_image(image_bytes: bytes, max_dim: int = 1600, quality: int = 85) -> bytes:
    """Corrige l'orientation EXIF smartphone et compresse l'image pour l'API."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = ImageOps.exif_transpose(img)
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()
    except Exception:
        return image_bytes

# ==============================================================================
# 6. CONFIGURATION PÉDAGOGIQUE
# ==============================================================================
active_api_key = get_persisted_key()

with st.sidebar:
    st.markdown("### 🎓 Paramètres de Khôlle")

    model_name = st.selectbox(
        "Modèle IA",
        options=["gemini-3.8-flash", "gemini-3.8-pro", "gemini-2.5-flash"],
        index=0,
        help="gemini-3.8-flash est le modèle officiel de dernière génération recommandé par Google pour une vitesse et une vision optimales.",
    )

    help_level = st.select_slider(
        "Niveau de guidage du colleur",
        options=["🎯 Concours Exigeant", "⚖️ Équilibré MPSI", "🆘 SOS Déblocage"],
        value="⚖️ Équilibré MPSI",
        help="Ajuste la finesse et la précision des indices donnés.",
    )

    if help_level == "🎯 Concours Exigeant":
        temperature_val = 0.10
        guidance_instruction = (
            "NIVEAU DE GUIDAGE : Rigueur maximale des concours X-ENS/Mines-Ponts. "
            "Donne uniquement des micro-questions d'orientation conceptuelles. Force l'élève à trouver par lui-même. "
            "Ne donne aucun résultat intermédiaire."
        )
    elif help_level == "⚖️ Équilibré MPSI":
        temperature_val = 0.15
        guidance_instruction = (
            "NIVEAU DE GUIDAGE : Progression socratique classique de prépa MPSI. "
            "Valide les acquis de l'élève, isole la difficulté et distille des indices graduels étape par étape."
        )
    else:  # SOS Déblocage
        temperature_val = 0.22
        guidance_instruction = (
            "NIVEAU DE GUIDAGE : L'élève est totalement bloqué. Sois très encourageant et plus explicite : "
            "rappelle le théorème précis du cours ou suggère l'astuce de calcul clé (changement de variable, fonction auxiliaire), "
            "mais laisse-lui toujours la rédaction et le calcul final."
        )

    st.divider()
    if st.button("🗑️ Nouvel exercice (Effacer tout)", use_container_width=True):
        reset_session()
        st.rerun()

    # Zone Admin protégée par mot de passe
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🔒 Administration & Clé API"):
        stored_hash = get_admin_hash()

        if not stored_hash:
            st.info("🔐 Créez votre mot de passe secret administrateur :")
            new_admin_pw = st.text_input("Définir un mot de passe", type="password", key="create_pw_in")
            if st.button("Enregistrer le mot de passe", use_container_width=True):
                if len(new_admin_pw) >= 4:
                    set_admin_hash(new_admin_pw)
                    st.session_state.admin_unlocked = True
                    st.success("Mot de passe enregistré !")
                    st.rerun()
                else:
                    st.warning("Choisissez au moins 4 caractères.")
        else:
            if not st.session_state.admin_unlocked:
                admin_pw_input = st.text_input("Mot de passe secret", type="password", key="login_pw_in")
                if st.button("Déverrouiller l'accès clé", use_container_width=True):
                    if hash_pw(admin_pw_input) == stored_hash:
                        st.session_state.admin_unlocked = True
                        st.rerun()
                    else:
                        st.error("Mot de passe incorrect.")
            else:
                st.success("🔓 Accès administrateur déverrouillé")
                masked_key = f"{active_api_key[:6]}...{active_api_key[-4:]}" if len(active_api_key) > 10 else "Non renseignée"
                st.caption(f"Clé active : `{masked_key}`")

                new_key_input = st.text_input(
                    "Modifier la clé API Gemini",
                    value=active_api_key,
                    type="password",
                    help="Obtenue sur https://aistudio.google.com",
                    key="admin_new_key_in",
                )
                if st.button("Sauvegarder définitivement", use_container_width=True):
                    set_persisted_key(new_key_input)
                    st.success("Clé enregistrée !")
                    st.rerun()

                if st.button("Reverrouiller", use_container_width=True):
                    st.session_state.admin_unlocked = False
                    st.rerun()

# ==============================================================================
# 7. PROMPT SYSTÈME SOCRATIQUE MPSI (HAUTE EXIGENCE MATHÉMATIQUE & OCR)
# ==============================================================================
SYSTEM_PROMPT = f"""Tu es un professeur et colleur de mathématiques d'élite en classe préparatoire MPSI (Maths Sup).
Tu es bienveillant, d'une rigueur formelle intraitable (niveau concours X-ENS, Mines-Ponts, CentraleSupélec) et extrêmement pédagogue.

### RÈGLE D'OR ABSOLUE :
**INTERDICTION FORMELLE de donner la solution finale, d'écrire une démonstration complète ou de faire les calculs à la place de l'élève**, même s'il insiste ou dit qu'il abandonne.

### FORMATAGE STRICT LATEX (CRUCIAL) :
- N'utilise JAMAIS les délimiteurs avec crochets comme \\[ ... \\] ou parenthèses \\( ... \\).
- Utilise UNIQUEMENT le dollar simple `$ ... $` pour les expressions mathématiques dans le texte (ex: `$f(x) = x^2$`, `$\\forall \\varepsilon > 0$`).
- Utilise le double dollar `$$ ... $$` sur des lignes dédiées pour les équations centrées.
- N'utilise AUCUN crochet de titre comme `[Indice 1]` ou `[Astuce]`. Rédige en prose fluide ou avec des titres épurés (ex: `### 💡 Indice de réflexion`).

{guidance_instruction}

### LECTURE DES PHOTOS D'ÉNONCÉ ET DE BROUILLON (OCR IMPITOYABLE) :
Quand une photo d'énoncé ou de brouillon t'est fournie :
1. **Transcris d'abord explicitement** la question ou formule clé concernée pour prouver ta lecture parfaite (attention aux indices $n+1$ vs $n$, exposants, inégalités strictes ou larges, domaines de définition).
2. Vérifie minutieusement chaque symbole manuscrit sur le brouillon de l'élève. Isole la première ligne exacte où se trouve l'erreur ou l'omission de rigueur.

### EXIGENCES DE RIGUEUR FORMELLE MPSI :
- Vérifie scrupuleusement l'ordre des quantificateurs ($\\forall \\varepsilon > 0, \\exists N \\in \\mathbb{{N}}$).
- Traque la distinction stricte entre implication $\\implies$ et équivalence $\\iff$.
- Rappelle les hypothèses exactes des théorèmes (intervalle connexe pour le TVI, continuité uniforme pour Heine, dimension finie pour le théorème du rang, sous-espace non vide $0_E \\in F$).
- Alerte sur les divisions par zéro ou les simplifications de matrices non inversibles.

### RÉPONSES AUX QUESTIONS DE L'ÉLÈVE :
Si l'élève te pose une question générale ("C'est quoi ce symbole ?", "Pourquoi ce théorème ne s'applique pas ?", "Comment démarrer ?") :
Réponds avec une limpidité pédagogique absolue, réexplique le concept en profondeur, mais termine TOUJOURS par une question de relance pour lui laisser la main sur son exercice.
"""

# ==============================================================================
# 8. MOTEUR D'APPEL GEMINI AVEC STREAMING
# ==============================================================================
def ask_socratic_tutor(user_text: str, media_bytes: bytes = None, media_mime: str = None) -> bool:
    """Envoie la requête à Gemini avec streaming et assainissement LaTeX."""
    if not active_api_key:
        st.error("⚠️ La clé API Gemini n'est pas encore enregistrée sur ce serveur. Entrez-la dans 'Administration' dans la barre latérale.")
        return False

    client = genai.Client(api_key=active_api_key)

    parts = []
    if media_bytes and media_mime:
        parts.append(types.Part.from_bytes(data=media_bytes, mime_type=media_mime))
    parts.append(types.Part.from_text(text=user_text))

    st.session_state.api_contents.append(
        types.Content(role="user", parts=parts)
    )

    with st.chat_message("assistant", avatar="👨‍🏫"):
        placeholder = st.empty()
        full_response = ""
        try:
            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=st.session_state.api_contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=temperature_val,
                ),
            )
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    clean_live = sanitize_latex(full_response)
                    placeholder.markdown(clean_live + " ▌")

            clean_final = sanitize_latex(full_response)
            placeholder.markdown(clean_final)

            st.session_state.messages.append({"role": "assistant", "content": clean_final})
            st.session_state.api_contents.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=clean_final)],
                )
            )
            return True
        except Exception as e:
            if st.session_state.api_contents:
                st.session_state.api_contents.pop()
            st.error(f"Erreur de communication : {e}")
            return False

# ==============================================================================
# 9. INTERFACE HERO 3D & ONGLETS
# ==============================================================================
st.markdown(
    """
    <div class="hero-3d-box">
        <div class="hero-3d-card">
            <span class="hero-3d-badge">🏛️ KHÔLLE VIRTUELLE MPSI • MATHS SUP</span>
            <h1 class="hero-3d-title">Tuteur Socratique d'Excellence</h1>
            <p class="hero-3d-subtitle">Résous tes exercices pas à pas avec ton colleur IA • Rigueur absolue des concours</p>
            <div class="hero-status-pills">
                <span class="hero-pill">⚡ Modèle : """ + model_name + """</span>
                <span class="hero-pill">🎯 Mode : """ + help_level + """</span>
                <span class="hero-pill">📐 Rendu : KaTeX Haute Définition</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

has_exercise = st.session_state.exercise_hash is not None

# Onglets 3D pour organiser le travail
tab_enonce, tab_brouillon, tab_aide = st.tabs([
    "📸 1. Énoncé de l'exercice",
    "📝 2. Brouillon manuscrit",
    "💡 3. Méthode de Khôlle",
])

with tab_enonce:
    if not has_exercise:
        st.info("👋 **Bienvenue en colle !** Charge la photo ou le PDF de ton exercice pour démarrer.")
    else:
        st.success("✅ **Énoncé en cours d'analyse.** Tu peux le remplacer à tout moment ci-dessous.")

    mode_import = st.radio(
        "Source de l'énoncé :",
        options=["📁 Fichier (Photo ou PDF)", "📷 Appareil photo smartphone/webcam"],
        horizontal=True,
        key="radio_source_enonce",
    )

    raw_data = None
    media_mime = None

    if mode_import == "📁 Fichier (Photo ou PDF)":
        f = st.file_uploader(
            "Sélectionner l'énoncé (PNG, JPG, PDF)",
            type=["png", "jpg", "jpeg", "webp", "pdf"],
            key="file_enonce_up",
        )
        if f:
            raw_data = f.getvalue()
            media_mime = f.type or "image/jpeg"
    else:
        cam = st.camera_input("Photographier l'énoncé", key="cam_enonce_in")
        if cam:
            raw_data = cam.getvalue()
            media_mime = "image/jpeg"

    if raw_data is not None:
        f_hash = hashlib.sha256(raw_data).hexdigest()
        if f_hash != st.session_state.exercise_hash:
            if not active_api_key:
                st.warning("⚠️ Renseignez d'abord votre clé API Gemini dans 'Administration' (menu latéral).")
            else:
                if media_mime.startswith("image/"):
                    processed_data = optimize_image(raw_data)
                    processed_mime = "image/jpeg"
                else:
                    processed_data = raw_data
                    processed_mime = media_mime

                st.session_state.exercise_hash = f_hash
                st.session_state.exercise_bytes = processed_data
                st.session_state.exercise_mime = processed_mime
                st.session_state.messages = []
                st.session_state.api_contents = []

                init_prompt = (
                    "Voici l'énoncé de mon exercice de mathématiques de MPSI. "
                    "Consignes d'analyse :\n"
                    "1. TRANSCRIPTION PRÉCISE : Identifie et retranscris textuellement l'énoncé de la première question à traiter pour confirmer la lecture exacte de chaque formule, indice et symbole.\n"
                    "2. THÈME : Précise le chapitre du programme de MPSI.\n"
                    "3. ORIENTATION : Pose-moi uniquement une première question d'orientation subtile ou rappelle-moi la définition clé pour m'aider à démarrer sans me donner la solution."
                )
                st.session_state.messages.append(
                    {"role": "user", "content": "📄 *[Énoncé de l'exercice soumis au colleur]*"}
                )
                if ask_socratic_tutor(init_prompt, media_bytes=processed_data, media_mime=processed_mime):
                    st.rerun()

    if st.session_state.exercise_bytes is not None:
        if st.session_state.exercise_mime.startswith("image/"):
            st.image(Image.open(io.BytesIO(st.session_state.exercise_bytes)), caption="Énoncé actif", use_container_width=True)
        else:
            st.info("📑 Polycopié PDF actif en mémoire.")

with tab_brouillon:
    if not has_exercise:
        st.caption("Charge d'abord un énoncé dans le premier onglet pour pouvoir soumettre tes calculs.")
    else:
        st.write("Tu as fait des calculs sur feuille et tu veux que le colleur vérifie ta démarche ?")
        brouillon_mode = st.radio(
            "Source du brouillon :",
            options=["📷 Prendre une photo", "📁 Importer une image"],
            horizontal=True,
            key="brouillon_choice_radio",
        )
        brouillon_raw = None
        if brouillon_mode == "📷 Prendre une photo":
            b_cam = st.camera_input("Photographier ta feuille de brouillon", key="brouillon_cam_in")
            if b_cam:
                brouillon_raw = b_cam.getvalue()
        else:
            b_file = st.file_uploader("Importer l'image du brouillon", type=["png", "jpg", "jpeg", "webp"], key="brouillon_file_in")
            if b_file:
                brouillon_raw = b_file.getvalue()

        if brouillon_raw is not None:
            b_hash = hashlib.sha256(brouillon_raw).hexdigest()
            if b_hash != st.session_state.draft_hash:
                if st.button("📤 Soumettre ce brouillon au colleur", use_container_width=True):
                    st.session_state.draft_hash = b_hash
                    opt_draft = optimize_image(brouillon_raw)
                    draft_prompt = (
                        "Voici la photo de mon brouillon et de mes calculs manuscrits pour cet exercice. "
                        "Analyse très attentivement mes écritures : dis-moi ce qui est rigoureux, pointe précisément la ligne "
                        "ou l'argument qui pose problème, et pose-moi une question pour m'aider à rectifier."
                    )
                    st.session_state.messages.append(
                        {"role": "user", "content": "📝 *[Photo de mes calculs manuscrits]*"}
                    )
                    with st.chat_message("user", avatar="🧑‍🎓"):
                        st.markdown("📝 *[Photo de mes calculs manuscrits]*")
                        st.image(Image.open(io.BytesIO(opt_draft)), caption="Mon brouillon manuscrit", width=300)

                    if ask_socratic_tutor(draft_prompt, media_bytes=opt_draft, media_mime="image/jpeg"):
                        st.rerun()

with tab_aide:
    st.markdown(
        """
        ### 🎯 Les Règles d'or de la Khôlle MPSI
        1. **Pas de solution toute cuite** : Le colleur ne te donnera jamais la réponse directe, son rôle est d'entraîner tes réflexes de concours.
        2. **Rigueur formelle** : Attention aux quantificateurs, aux ensembles de définition et aux hypothèses des théorèmes (continuité, dimension finie, etc.).
        3. **Pose toutes tes questions** : N'hésite pas à demander des précisions sur une définition ou sur ce qu'attend l'énoncé.
        4. **Utilise les boutons tactiles** : En bas du chat, clique sur les boutons 3D pour demander un indice ciblé ou un rappel de cours.
        """
    )

# ==============================================================================
# 10. DIALOGUE DU CHAT & BOUTONS D'ACTION RAPIDE
# ==============================================================================
for msg in st.session_state.messages:
    avatar = "👨‍🏫" if msg["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

quick_prompt = None
if has_exercise and len(st.session_state.messages) > 0:
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💡 Indice suivant", use_container_width=True):
            quick_prompt = "Je bloque toujours à cette étape. Peux-tu me donner l'indice suivant sans me donner la réponse ?"
    with c2:
        if st.button("📖 Rappel de cours", use_container_width=True):
            quick_prompt = "Peux-tu me rappeler la définition ou le théorème précis du cours utile ici ?"

    c3, c4 = st.columns(2)
    with c3:
        if st.button("🔎 Vérifie ma rigueur", use_container_width=True):
            quick_prompt = "Peux-tu vérifier si mon dernier raisonnement est formellement rigoureux au sens des exigences de MPSI ?"
    with c4:
        if st.button("🏆 J'ai trouvé la solution !", use_container_width=True):
            quick_prompt = "Je pense avoir abouti ! Peux-tu valider le résultat final et me résumer l'astuce de khôlle à retenir ?"

# Barre de saisie libre
user_text = st.chat_input("Pose une question sur l'énoncé, propose une piste ou réponds au colleur...")
final_prompt = quick_prompt or user_text

if final_prompt:
    if not has_exercise:
        st.warning("👆 Charge d'abord l'énoncé de l'exercice ci-dessus !")
    else:
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(final_prompt)

        success = ask_socratic_tutor(final_prompt)
        if success:
            st.rerun()
        else:
            st.session_state.messages.pop()
