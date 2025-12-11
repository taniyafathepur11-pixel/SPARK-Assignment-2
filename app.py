from flask import Flask, request, jsonify, render_template
import os
import sys
from werkzeug.utils import secure_filename
from spark_analyzer import analyze_student_marks
from simple_analyzer import analyze_student_marks_simple

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '../data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
    
    try:
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file using Spark analyzer
        try:
            results = analyze_student_marks(file_path)
            
            # Return results as JSON
            return jsonify({
                'success': True,
                'message': 'File uploaded and analyzed successfully',
                'data': results
            })
        except Exception as e:
            # Handle specific Spark errors
            error_msg = str(e)
            if 'JavaSparkContext' in error_msg and 'getSubject is not supported' in error_msg:
                # Try fallback to simple analyzer
                try:
                    results = analyze_student_marks_simple(file_path)
                    return jsonify({
                        'success': True,
                        'message': 'File uploaded and analyzed successfully (using simplified analyzer)',
                        'data': results
                    })
                except Exception as fallback_error:
                    error_msg = f'Spark error: {str(e)}. Fallback analyzer error: {str(fallback_error)}'
            return jsonify({
                'success': False,
                'error': f'Error analyzing file: {error_msg}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing file: {str(e)}'
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    try:
        # Get the latest file in the upload folder
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not files:
            return jsonify({'error': 'No files found for analysis'}), 400
        
        # Get the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], f)))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)
        
        # Process the file using Spark analyzer
        try:
            results = analyze_student_marks(file_path)
            
            # Return results as JSON
            return jsonify({
                'success': True,
                'message': 'Data analyzed successfully',
                'data': results
            })
        except Exception as e:
            # Handle specific Spark errors
            error_msg = str(e)
            if 'JavaSparkContext' in error_msg and 'getSubject is not supported' in error_msg:
                # Try fallback to simple analyzer
                try:
                    results = analyze_student_marks_simple(file_path)
                    return jsonify({
                        'success': True,
                        'message': 'Data analyzed successfully (using simplified analyzer)',
                        'data': results
                    })
                except Exception as fallback_error:
                    error_msg = f'Spark error: {str(e)}. Fallback analyzer error: {str(fallback_error)}'
            return jsonify({
                'success': False,
                'error': f'Error analyzing data: {error_msg}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error analyzing data: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)