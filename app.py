import os
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import tempfile
from PIL import Image
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def process_pdf(input_pdf, rows, cols, selected_slides):
    # Create a temporary file for the output
    output = io.BytesIO()
    
    # Open the PDF with PyMuPDF
    doc = fitz.open(input_pdf)
    
    # Create a new PDF with ReportLab
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    
    # Calculate dimensions for the grid
    slide_width = width / cols
    slide_height = height / rows
    
    # Process each page
    for i, page_num in enumerate(selected_slides):
        if i % (rows * cols) == 0 and i > 0:
            c.showPage()
        
        # Get the current position in the grid
        row = (i % (rows * cols)) // cols
        col = (i % (rows * cols)) % cols
        
        # Calculate position
        x = col * slide_width
        y = height - (row + 1) * slide_height
        
        # Get the page from the input PDF
        page = doc[page_num - 1]
        
        # Convert page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
        img_data = pix.tobytes("png")
        
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
            temp_img.write(img_data)
            temp_img_path = temp_img.name
        
        # Draw the image
        c.drawImage(temp_img_path, x, y, width=slide_width, height=slide_height)
        
        # Clean up the temporary image file
        os.unlink(temp_img_path)
    
    c.save()
    output.seek(0)
    doc.close()
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Get the number of pages
    reader = PdfReader(filepath)
    total_pages = len(reader.pages)
    
    return jsonify({
        'total_pages': total_pages,
        'filename': filename
    })

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    filename = data['filename']
    rows = int(data['rows'])
    cols = int(data['cols'])
    selected_slides = [int(x) for x in data['selected_slides']]
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Process the PDF
    output = process_pdf(filepath, rows, cols, selected_slides)
    
    # Clean up the input file
    os.remove(filepath)
    
    # Return the processed PDF
    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='processed_presentation.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True) 