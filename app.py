import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    image_names = os.listdir('./static/images')
    # Notice that 'images' has been removed from the join
    images = [image.replace('\\', '/') for image in image_names]
    return render_template('home.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
