# Slide Grid

A web application that converts PDF presentations into a grid layout on A4 paper. This tool allows you to arrange multiple slides per page in a customizable grid format.

🔗 **Live Demo**: [https://slide-grid.onrender.com/](https://slide-grid.onrender.com/)

## Features

- 📤 Upload PDF presentations
- ⚙️ Customize grid layout (rows and columns)
- ✅ Select specific slides to include/exclude
- 📄 Automatic A4 page size optimization
- 🎨 Modern and responsive user interface
- 💾 Download processed PDF files
- 🔄 Real-time slide selection
- 📱 Mobile-friendly design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/slide-grid.git
cd slide-grid
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload your PDF presentation and follow the on-screen instructions:
   - Select the number of rows and columns for the grid layout
   - Choose which slides to include in the final output
   - Click "Generate PDF" to create and download the processed file

## How It Works

1. **Upload**: Select your PDF presentation file
2. **Configure**: Choose the number of rows and columns for the grid
3. **Select**: Pick which slides to include in the final output
4. **Generate**: Create and download the new PDF with slides arranged in a grid

## Technical Details

- Built with Flask
- Uses PyPDF2 for PDF manipulation
- ReportLab for PDF generation
- PyMuPDF for high-quality PDF to image conversion
- Bootstrap 5 for responsive design

## Requirements

- Python 3.10 or higher
- Flask
- PyPDF2
- ReportLab
- PyMuPDF
- Pillow
- Werkzeug
- Gunicorn

## Development

To run tests:
```bash
python -m pytest tests/
```

To check code style:
```bash
flake8 .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 