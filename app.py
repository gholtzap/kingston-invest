import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    big_tech_names = os.listdir('./static/images/big-tech')
    cancelled_names = os.listdir('./static/images/cancelled')
    misc_names = os.listdir('./static/images/misc')
    
    big_tech_images = [image.replace('\\', '/') for image in big_tech_names]
    cancelled_images = [image.replace('\\', '/') for image in cancelled_names]
    misc_images = [image.replace('\\', '/') for image in misc_names]
    
    return render_template('home.html', big_tech_images=big_tech_images,cancelled_images=cancelled_images,misc_images=misc_images)

if __name__ == '__main__':
    app.run(debug=True)
