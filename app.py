# app.py

import io
from flask import Flask, render_template, request, send_file
from docx import Document

# --- 1. FLASK APPLICATION SETUP ---
app = Flask(__name__)

# --- Function to generate the DOCX content ---
def create_docx(data):
    """
    Creates the DOCX document using the data submitted from the web form.
    Returns the document object and the final filename.
    """
    doc = Document()

    # --- TITLE ---
    doc.add_heading('CHILDREN’S BOOK ILLUSTRATION AGREEMENT', 0)
    doc.add_paragraph('(Draft for creative practice only — not legal advice)')
    doc.add_paragraph(f'Governing Law: {data.get("governing_law", "Indiana")}')

    # --- PARTIES ---
    doc.add_heading('Parties', level=1)
    doc.add_paragraph('This Agreement is made between:')
    doc.add_paragraph(f'Author/Creator: {data.get("author_name", "[Your Name]")}, residing in {data.get("author_city_state", "[City, State]")}')
    doc.add_paragraph(f'Illustrator (Minor): {data.get("illustrator_name", "[Child’s Name]")}')
    doc.add_paragraph(f'Parent/Legal Guardian: {data.get("guardian_name", "[Parent’s Name]")}, residing in {data.get("guardian_city_state", "[City, State]")}')
    doc.add_paragraph(f'Effective as of: {data.get("effective_date", "[Date]")}')
    
    # --- SECTIONS (Simplified Example) ---
    doc.add_heading('1. Scope of Work', level=1)
    doc.add_paragraph(f'The Illustrator will create original artwork for a children’s book currently titled "{data.get("book_title", "[Book Title]")}". Deliverables: {data.get("deliverables", "[cover, page spreads, etc.]")}')

    doc.add_heading('2. Compensation', level=1)
    doc.add_paragraph(f'Author agrees to pay Illustrator a total of ${data.get("total_compensation", "[amount USD]")} USD.')
    # ... You would add the rest of your agreement text here, using data.get() for every variable ...

    # --- SIGNATURE CANVAS (Simplified) ---
    doc.add_heading('Signature Canvas', level=1)
    doc.add_paragraph(f'Author/Creator Printed Name: {data.get("author_name", "________________")}\nDate: _____________________________________')
    doc.add_paragraph(f'Parent/Legal Guardian Printed Name: {data.get("guardian_name", "________________")}\nDate: _____________________________________')

    # Use a BytesIO buffer to hold the document in memory (required for web downloads)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0) # Rewind the stream to the beginning
    
    filename = f"Illustration_Agreement_for_{data.get('book_title', 'Book').replace(' ', '_')}.docx"
    
    return file_stream, filename

# --- 2. WEB ROUTES (The two main pages/actions) ---

@app.route('/')
def index():
    """
    The landing page route. Renders the HTML form for user input.
    """
    # The 'templates/form.html' file will be rendered here
    return render_template('form.html')
    
@app.route('/generate', methods=['POST'])
def generate():
    """
    The form submission route.
    1. Grabs all data submitted via the POST request.
    2. Calls create_docx to generate the file in memory.
    3. Sends the generated file back to the user's browser for download.
    """
    # request.form contains all the data submitted from the HTML form
    form_data = request.form 
    
    # Get the file stream and the intended filename
    file_stream, filename = create_docx(form_data)
    
    # Use Flask's send_file to push the document to the user's browser
    return send_file(
        file_stream, 
        as_attachment=True, 
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

# --- 3. RUN THE APPLICATION ---

if __name__ == '__main__':
    # When running locally (python app.py), this line is used
    # On Render, the 'gunicorn app:app' command handles starting the app.
    app.run(debug=True)