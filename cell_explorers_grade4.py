import streamlit as st
import pandas as pd
from datetime import datetime
import html

st.set_page_config(page_title="Cell Explorers Lab", page_icon="🔬", layout="wide")

# ============================================================
# ✏️ TEACHER EDIT ZONE
# Edit any question independently.
# Change: question, options, answer, hint, fact, organelle, or cell.
# Keep "answer" exactly the same as one item in "options".
# ============================================================

QUESTIONS = [
    {
        "organelle": "Nucleus", "cell": "Both",
        "question": "You found the cell's control center! What is the main job of the nucleus?",
        "options": ["It controls the activities of the cell", "It makes food using sunlight", "It stores water", "It forms the outside wall"],
        "answer": "It controls the activities of the cell",
        "hint": "Think of the nucleus as the cell's boss or control room.",
        "fact": "The nucleus controls many cell activities and contains genetic information."
    },
    {
        "organelle": "Cell membrane", "cell": "Both",
        "question": "Look at the thin boundary around the cell. What does the cell membrane do?",
        "options": ["Controls what enters and leaves the cell", "Makes food from sunlight", "Stores only DNA", "Gives plants their green color"],
        "answer": "Controls what enters and leaves the cell",
        "hint": "Imagine a security gate deciding what may go in or out.",
        "fact": "The cell membrane is a thin, flexible boundary that controls what enters and leaves the cell."
    },
    {
        "organelle": "Cytoplasm", "cell": "Both",
        "question": "The organelles are surrounded by a jelly-like material. What is it called?",
        "options": ["Cytoplasm", "Cell wall", "Chloroplast", "Nucleus"],
        "answer": "Cytoplasm",
        "hint": "It fills much of the inside of the cell and surrounds the organelles.",
        "fact": "Cytoplasm is the jelly-like material inside the cell where organelles are found."
    },
    {
        "organelle": "Mitochondrion", "cell": "Both",
        "question": "This bean-shaped organelle has folds inside. What is its main job?",
        "options": ["Releases energy from food for the cell", "Controls what enters the cell", "Makes the plant cell rigid", "Stores genetic information"],
        "answer": "Releases energy from food for the cell",
        "hint": "It is often called the powerhouse of the cell.",
        "fact": "Mitochondria release usable energy from food."
    },
    {
        "organelle": "Vacuole", "cell": "Plant",
        "question": "In this plant cell, you see a large sac-like space. What is an important job of the vacuole?",
        "options": ["Stores water and other materials", "Controls the whole cell", "Makes energy from food", "Controls what enters and leaves the cell"],
        "answer": "Stores water and other materials",
        "hint": "Think of it as a storage tank. Plant cells usually have one large central vacuole.",
        "fact": "The large central vacuole stores water and other materials and helps support the plant cell."
    },
    {
        "organelle": "Cell wall", "cell": "Plant",
        "question": "You notice a thick, strong layer outside the plant cell membrane. What is it?",
        "options": ["Cell wall", "Cytoplasm", "Nucleus", "Mitochondrion"],
        "answer": "Cell wall",
        "hint": "This strong outer layer helps the plant cell keep its shape.",
        "fact": "The cell wall is a strong layer outside the cell membrane that supports and protects plant cells."
    },
    {
        "organelle": "Chloroplast", "cell": "Plant",
        "question": "These green oval organelles capture light. What do chloroplasts help the plant do?",
        "options": ["Make food using light energy", "Control all cell activities", "Store genetic information", "Control what enters and leaves"],
        "answer": "Make food using light energy",
        "hint": "Chloroplasts contain chlorophyll and are found in plant cells.",
        "fact": "Chloroplasts contain chlorophyll and help plants make food by photosynthesis."
    },
    {
        "organelle": "Cell wall", "cell": "Plant",
        "question": "Which structure helps a plant cell have a more fixed, box-like shape?",
        "options": ["Cell wall", "Cytoplasm", "Nucleus", "Cell membrane only"],
        "answer": "Cell wall",
        "hint": "Look for the thick outer boundary in the plant-cell specimen.",
        "fact": "The cell wall gives plant cells support and a more fixed shape."
    },
    {
        "organelle": "Chloroplast", "cell": "Plant",
        "question": "You compare the two slides. Which structure is normally found in plant cells but not animal cells?",
        "options": ["Chloroplast", "Nucleus", "Cell membrane", "Cytoplasm"],
        "answer": "Chloroplast",
        "hint": "Which organelle helps a plant capture light to make food?",
        "fact": "Plant cells have chloroplasts for photosynthesis; animal cells do not."
    },
    {
        "organelle": "Nucleus", "cell": "Both",
        "question": "Final discovery! Which group of structures can be found in BOTH plant and animal cells?",
        "options": ["Nucleus, cell membrane and cytoplasm", "Cell wall, chloroplast and large central vacuole", "Cell wall, nucleus and chloroplast", "Chloroplast, cell membrane and cell wall"],
        "answer": "Nucleus, cell membrane and cytoplasm",
        "hint": "Think about the structures you observed on BOTH microscope slides.",
        "fact": "Both plant and animal cells have a nucleus, cell membrane and cytoplasm."
    }
]

# ============================================================
# SIMPLIFIED SCIENTIFIC TEACHING DIAGRAMS
# Built into the app: no external image links are needed.
# ============================================================

def organelle_svg(name):
    drawings = {
        "Nucleus": '<circle cx="160" cy="100" r="62" fill="#c7b5ff" stroke="#563a9c" stroke-width="6"/><circle cx="160" cy="100" r="22" fill="#7652c7"/><circle cx="126" cy="72" r="6" fill="#7652c7"/><circle cx="192" cy="82" r="5" fill="#7652c7"/>',
        "Cell membrane": '<ellipse cx="160" cy="100" rx="120" ry="70" fill="#eefcff" stroke="#3f9eae" stroke-width="10"/><ellipse cx="160" cy="100" rx="107" ry="57" fill="none" stroke="#91d5df" stroke-width="3"/>',
        "Cytoplasm": '<ellipse cx="160" cy="100" rx="120" ry="70" fill="#dff7ef" stroke="#489b7c" stroke-width="5"/><circle cx="125" cy="90" r="28" fill="#c7b5ff" stroke="#563a9c" stroke-width="4"/><ellipse cx="205" cy="80" rx="24" ry="13" fill="#ffb36b" stroke="#a85c22" stroke-width="4"/>',
        "Mitochondrion": '<path d="M65,105 C65,45 130,35 190,55 C255,75 270,130 220,155 C160,185 65,165 65,105 Z" fill="#ffb36b" stroke="#a85c22" stroke-width="6"/><path d="M95,80 C120,55 135,120 160,85 S200,65 225,105 S205,145 175,125 S135,145 110,120" fill="none" stroke="#a85c22" stroke-width="5"/>',
        "Vacuole": '<path d="M65,45 Q160,18 250,55 Q280,110 245,158 Q155,188 65,150 Q35,95 65,45 Z" fill="#bde8ff" stroke="#4385b5" stroke-width="6"/><path d="M90,65 Q160,45 225,70 Q240,105 220,135 Q155,155 90,130 Q70,100 90,65 Z" fill="#e8f8ff"/>',
        "Cell wall": '<rect x="45" y="30" width="230" height="140" rx="8" fill="#eef8d5" stroke="#668d3c" stroke-width="13"/><rect x="62" y="47" width="196" height="106" rx="12" fill="#f8ffe8" stroke="#94c35a" stroke-width="4"/>',
        "Chloroplast": '<ellipse cx="160" cy="100" rx="105" ry="62" fill="#8ed081" stroke="#2f7d32" stroke-width="6"/><g fill="#3f9142" stroke="#246b27" stroke-width="2"><rect x="95" y="67" width="38" height="7" rx="3"/><rect x="95" y="77" width="38" height="7" rx="3"/><rect x="95" y="87" width="38" height="7" rx="3"/><rect x="165" y="105" width="42" height="7" rx="3"/><rect x="165" y="115" width="42" height="7" rx="3"/><rect x="165" y="125" width="42" height="7" rx="3"/></g>'
    }
    body = drawings.get(name, drawings["Nucleus"])
    return f'<div class="scope"><svg viewBox="0 0 320 200" width="100%" height="210" role="img" aria-label="{html.escape(name)} simplified diagram"><circle cx="160" cy="100" r="96" fill="#fbfdff" stroke="#20252b" stroke-width="8"/><circle cx="160" cy="100" r="88" fill="#ffffff" stroke="#dce4eb" stroke-width="3"/>{body}</svg></div>'

def whole_cell_svg(kind):
    if kind == "Plant":
        return '<svg viewBox="0 0 420 280" width="100%" role="img" aria-label="Simplified plant cell"><rect x="35" y="35" width="350" height="210" rx="20" fill="#e9f7d9" stroke="#608c3c" stroke-width="12"/><rect x="51" y="51" width="318" height="178" rx="18" fill="#eafaff" stroke="#4ba3ad" stroke-width="5"/><ellipse cx="215" cy="145" rx="92" ry="62" fill="#bde8ff" stroke="#4385b5" stroke-width="4"/><circle cx="92" cy="95" r="30" fill="#c7b5ff" stroke="#563a9c" stroke-width="4"/><g fill="#78c66b" stroke="#2f7d32" stroke-width="3"><ellipse cx="110" cy="185" rx="27" ry="13"/><ellipse cx="320" cy="92" rx="27" ry="13"/><ellipse cx="315" cy="190" rx="27" ry="13"/></g><ellipse cx="330" cy="145" rx="24" ry="13" fill="#ffb36b" stroke="#a85c22" stroke-width="3"/></svg>'
    return '<svg viewBox="0 0 420 280" width="100%" role="img" aria-label="Simplified animal cell"><path d="M70,70 C120,25 230,25 325,65 C390,95 380,190 310,225 C220,265 100,240 55,175 C30,135 38,98 70,70 Z" fill="#eafaff" stroke="#4ba3ad" stroke-width="7"/><circle cx="175" cy="130" r="47" fill="#c7b5ff" stroke="#563a9c" stroke-width="4"/><circle cx="175" cy="130" r="16" fill="#7652c7"/><ellipse cx="275" cy="95" rx="35" ry="17" fill="#ffb36b" stroke="#a85c22" stroke-width="4"/><path d="M250,92 Q265,75 280,96 T302,95" fill="none" stroke="#a85c22" stroke-width="3"/><ellipse cx="115" cy="190" rx="30" ry="16" fill="#ffb36b" stroke="#a85c22" stroke-width="4"/></svg>'

st.markdown('''
<style>
.stApp { background: linear-gradient(180deg,#f5fbff 0%,#fffdf5 100%); }
.block-container { max-width: 1050px; padding-top: 1.5rem; }
.lab-card { background:white; border:1px solid #dbe7ef; border-radius:22px; padding:22px; box-shadow:0 7px 24px rgba(40,70,90,.08); margin-bottom:18px; }
.scope { max-width:420px; margin:auto; padding:6px; }
.badge { display:inline-block; padding:5px 11px; border-radius:999px; background:#e9f6ff; font-weight:700; margin-right:5px; }
.small-note { color:#52606d; font-size:.92rem; }
</style>
''', unsafe_allow_html=True)

if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "section" not in st.session_state:
    st.session_state.section = None

st.title("🔬 Cell Explorers Lab")
st.subheader("Grade 4 Discovery Mission: Plant & Animal Cells")
st.write("Explore the microscope specimens, use the clues, and identify the names, structures, and jobs of cell organelles.")

with st.container(border=True):
    st.markdown("### 🧪 Scientist Check-In")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        name_input = st.text_input("Student name", value=st.session_state.student_name, disabled=st.session_state.started)
    with c2:
        st.selectbox("Grade", ["Grade 4"], disabled=st.session_state.started)
    with c3:
        section_input = st.selectbox("Section", ["A", "B", "C"], index=None if st.session_state.section is None else ["A","B","C"].index(st.session_state.section), disabled=st.session_state.started, placeholder="Choose")

    if not st.session_state.started:
        if st.button("🚀 Enter the Lab", type="primary", use_container_width=True):
            if not name_input.strip() or section_input is None:
                st.error("Please enter your name and choose your section first.")
            else:
                st.session_state.student_name = name_input.strip()
                st.session_state.section = section_input
                st.session_state.started = True
                st.rerun()

if st.session_state.started:
    st.info("🧫 **Mission:** 10 microscope discoveries. Each correct answer = **1 mark**. Total = **10 marks**.")

    st.markdown("### 👀 First, compare the two specimens")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="lab-card"><h4>🌿 Plant Cell</h4>' + whole_cell_svg("Plant") + '<p class="small-note">Look carefully at its fixed shape, thick outer wall, green chloroplasts, and large vacuole.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="lab-card"><h4>🐾 Animal Cell</h4>' + whole_cell_svg("Animal") + '<p class="small-note">Look at its flexible boundary. It has no cell wall and no chloroplasts.</p></div>', unsafe_allow_html=True)

    st.markdown("## 🔍 Microscope Discovery Stations")

    answers = {}
    for i, q in enumerate(QUESTIONS, start=1):
        st.markdown(f"### Station {i} of {len(QUESTIONS)}")
        a, b = st.columns([1, 1.35])
        with a:
            st.markdown(organelle_svg(q["organelle"]), unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center"><span class="badge">{q["cell"]} cell</span><span class="badge">Focus: {q["organelle"]}</span></div>', unsafe_allow_html=True)
        with b:
            st.markdown(f"**Discovery question:** {q['question']}")
            with st.expander("💡 Open discovery clue"):
                st.write("🔎 " + q["hint"])
            answers[i] = st.radio(f"Choose one answer for Station {i}:", q["options"], index=None, key=f"q_{i}", disabled=st.session_state.submitted)
            if st.session_state.submitted:
                if answers[i] == q["answer"]:
                    st.success("✅ Correct! " + q["fact"])
                else:
                    st.error(f"❌ Correct answer: **{q['answer']}**")
                    st.caption(q["fact"])
        st.markdown("---")

    if not st.session_state.submitted:
        unanswered = sum(answers[i] is None for i in answers)
        if unanswered:
            st.warning(f"🧭 You still have {unanswered} station(s) to answer.")
        if st.button("📨 Submit My Lab Mission", type="primary", use_container_width=True):
            if unanswered:
                st.error("Please answer every station before submitting.")
            else:
                st.session_state.submitted = True
                st.rerun()

    if st.session_state.submitted:
        score = sum(st.session_state.get(f"q_{i}") == q["answer"] for i, q in enumerate(QUESTIONS, start=1))
        st.balloons()
        st.markdown("## 🏆 Lab Mission Complete!")
        st.metric("Final Grade", f"{score} / {len(QUESTIONS)}")
        if score >= 9:
            st.success("🌟 Outstanding Cell Explorer!")
        elif score >= 7:
            st.success("👏 Great work, Scientist!")
        elif score >= 5:
            st.info("🧠 Good start! Review the microscope clues and organelle jobs.")
        else:
            st.warning("🔬 Keep exploring! Review the organelles with your teacher.")

        result = pd.DataFrame([{
            "Student Name": st.session_state.student_name,
            "Grade": "Grade 4",
            "Section": st.session_state.section,
            "Score": score,
            "Total": len(QUESTIONS),
            "Submitted At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        st.download_button("⬇️ Download Result", result.to_csv(index=False).encode("utf-8"),
                           file_name=f"{st.session_state.student_name.replace(' ','_')}_cell_lab_result.csv",
                           mime="text/csv", use_container_width=True)
        st.caption("This version grades automatically. For one teacher dashboard that collects every student's result, connect the app to a shared database or Google Sheet.")
