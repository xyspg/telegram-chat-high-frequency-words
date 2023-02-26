import json
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from flask import Flask, render_template, request

# 读取JSON文件
with open('result.json', 'r') as f:
    chat_data = json.load(f)

# 合并所有消息的文本
all_text = ' '.join([entity['text'] for msg in chat_data['messages'] for entity in msg['text_entities'] if entity['type'] == 'plain'])

# 分词
tokens = word_tokenize(all_text)

# 创建词频分布
fdist = FreqDist(tokens)

# Flask web应用
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Save the file to disk
        uploaded_file.save(uploaded_file.filename)
        # Load the data from the uploaded file
        with open(uploaded_file.filename, 'r') as f:
            chat_data = json.load(f)
        # Process the data as before
        all_text = ' '.join([entity['text'] for msg in chat_data['messages'] for entity in msg['text_entities'] if entity['type'] == 'plain'])
        tokens = word_tokenize(all_text)
        fdist = FreqDist(tokens)
        top_words = fdist.most_common(100)
        return render_template('upload.html', top_words=top_words)
    else:
        return '未选择文件'

# 运行程序
if __name__ == '__main__':
    app.run()
