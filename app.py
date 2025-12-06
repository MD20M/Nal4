from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
FONT_SIZE = 40
TEXT_COLOR = (255, 255, 255)  # Bela
STROKE_COLOR = (0, 0, 0)  # Črna
STROKE_WIDTH = 2

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def add_text_to_image(image_path, top_text, bottom_text):

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE)
    except:
        font = ImageFont.load_default()
    
    img_width, img_height = img.size
    
    def get_text_position(text, position='top'):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (img_width - text_width) / 2
        
        if position == 'top':
            y = 10
        else:  
            y = img_height - text_height - 10
            
        return (x, y)
    
    if top_text:
        top_text = top_text.upper()
        pos = get_text_position(top_text, 'top')
        draw.text(pos, top_text, font=font, fill=TEXT_COLOR, 
                 stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)
    
    if bottom_text:
        bottom_text = bottom_text.upper()
        pos = get_text_position(bottom_text, 'bottom')
        draw.text(pos, bottom_text, font=font, fill=TEXT_COLOR,
                 stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)
        
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_meme():
    if 'image' not in request.files:
        return 'Napaka: Datoteka ni bila naložena', 400
    
    file = request.files['image']
    
    if file.filename == '':
        return 'Napaka: Datoteka ni bila izbrana', 400
    
    top_text = request.form.get('top_text', '')
    bottom_text = request.form.get('bottom_text', '')
    
    temp_path = os.path.join(UPLOAD_FOLDER, 'temp_upload.jpg')
    file.save(temp_path)
    
    meme_image = add_text_to_image(temp_path, top_text, bottom_text)
    
    img_io = io.BytesIO()
    meme_image.save(img_io, 'JPEG', quality=95)
    img_io.seek(0)
    
    os.remove(temp_path)
    
    return send_file(img_io, mimetype='image/jpeg', as_attachment=False, 
                    download_name='meme.jpg')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
