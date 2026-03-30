import base64
import re
import tempfile
import textwrap
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def render():
    if "note" not in st.session_state:
        return

    st.divider()
    st.subheader("📄 Download Clinical Note")

    if st.button("Download Clinical Note as PDF", key="pdf_button"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                c = canvas.Canvas(tmpfile.name, pagesize=letter)
                width, height = letter
                margin_left = 72
                max_chars = 90

                # Header
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin_left, height - 72, "AI Medical Scribe - Clinical Note")
                c.drawString(margin_left, height - 100, f"Doctor: {st.session_state['doctor_name']} ({st.session_state['specialty']})")
                c.drawString(margin_left, height - 118, f"Patient: {st.session_state['patient_name']} | Age/Gender: {st.session_state['patient_age']}")
                c.drawString(margin_left, height - 136, f"Date: {st.session_state['visit_date']}")

                # Note body
                text = st.session_state["note"]
                y = height - 170

                def new_page():
                    c.showPage()
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(margin_left, height - 72, "AI Medical Scribe - Clinical Note (cont.)")
                    c.setFont("Helvetica", 11)
                    return height - 100

                c.setFont("Helvetica", 11)
                for raw_line in text.split("\n"):
                    clean = re.sub(r"\*\*(.+?)\*\*", r"\1", raw_line)
                    is_header = bool(re.match(r"^\*\*.+\*\*$", raw_line.strip()))
                    wrapped = textwrap.wrap(clean, width=max_chars) if clean.strip() else [""]

                    for i, sub_line in enumerate(wrapped):
                        if y < 72:
                            y = new_page()
                        if is_header and i == 0:
                            c.setFont("Helvetica-Bold", 11)
                            c.drawString(margin_left, y, sub_line)
                            c.setFont("Helvetica", 11)
                        else:
                            c.drawString(margin_left, y, sub_line)
                        y -= 15

                c.save()

                with open(tmpfile.name, "rb") as pdf_file:
                    b64 = base64.b64encode(pdf_file.read()).decode("utf-8")

                href = f'<a href="data:application/pdf;base64,{b64}" download="Clinical-Note.pdf">📥 Click here to download your clinical note</a>'
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error creating PDF: {e}")