import os
from flask import Flask, render_template, request, redirect
from collections import namedtuple

app = Flask(__name__)
BOOK = 'static/book.txt'
USERDATA = 'static/userData.txt'

LOGIN_HTML = 'login.html'
INDEX_HTML = 'index.html'
CHART_HTML = 'chart.html'
BOOK_HTML = 'book.html'
BOOKDATA_HTML = 'bookdata.html'

@app.route('/') # / url 요청이 들어온다면 해당 함수를 실행
def first(): # index.html을 반환함.
        return render_template(LOGIN_HTML)

@app.route('/main', methods=['post'])
def login(): # index.html을 반환함.
    id = request.form['id'] 
    pw = request.form['pw']

    with open(USERDATA, 'r') as file:
        for line in file:
            line = line.rstrip().split(',')
            if line[0] == id and line[1] == pw:
                return render_template(INDEX_HTML)
        return redirect('/')
        
@app.route('/main', methods=['get'])
def main(): # index.html을 반환함.
    menu = request.args.get('select')
    if menu == 'intro':
        return render_template(INDEX_HTML)
    elif menu == 'book':
        bookTitle = []
        bookPublisher = []
        bookWriter = []
        bookLen = []
        bookMemo = []
        
        with open(BOOK, 'r') as file:
            for line in file:
                line = line.rstrip().split(',')
                bookTitle.append(line[0])
                bookPublisher.append(line[1])
                bookWriter.append(line[2])
                bookLen.append(line[3])
                bookMemo.append(line[4])
            
        return render_template(BOOK_HTML, title = bookTitle, publisher = bookPublisher, writer = bookWriter, len = bookLen, memo = bookMemo)
    
    elif menu == 'graph':
        return render_template(CHART_HTML)
    
    elif menu == 'data':
        bookTitle = []
        bookPublisher = []
        bookWriter = []
        bookLen = []
        bookMemo = []
        
        with open(BOOK, 'r') as file:
            for line in file:
                line = line.rstrip().split(',')
                bookTitle.append(line[0])
                bookPublisher.append(line[1])
                bookWriter.append(line[2])
                bookLen.append(line[3])
                bookMemo.append(line[4])

        return render_template(BOOKDATA_HTML, title = bookTitle, publisher = bookPublisher, writer = bookWriter, len = bookLen, memo = bookMemo)
    
    else:
        return redirect('/')

@app.route('/modify', methods=['get'])
def modify(): # 전화번호 검색
    bookTitle = []
    bookPublisher = []
    bookWriter = []
    bookLength = []
    bookMemo = []

    i = 0
    type = request.args.get('type')
    id = request.args.get('id')
    title = request.args.get('title')
    publisher = request.args.get('publisher')
    writer = request.args.get('writer')
    length = request.args.get('len')
    memo = request.args.get('memo')
    
    with open(BOOK, 'r') as file:
        for line in file:
            line = line.rstrip().split(',')
            if i == int(id):
                if type == 'save':
                    bookTitle.append(title)
                    bookPublisher.append(publisher)
                    bookWriter.append(writer)
                    bookLength.append(length)
                    bookMemo.append(memo)
                    oldName = os.path.join("static/pic", line[0] + ".jpg")
                    newName = os.path.join("static/pic", title + ".jpg")
                    os.rename(oldName, newName)
                    
            else:
                bookTitle.append(line[0])
                bookPublisher.append(line[1])
                bookWriter.append(line[2])
                bookLength.append(line[3])
                bookMemo.append(line[4])
            i = int(i) + 1
    
    file = open(BOOK, 'w')
    for i in range(len(bookTitle)):
        data = '%s,%s,%s,%s,%s\n' % (bookTitle[i], bookPublisher[i], bookWriter[i], bookLength[i], bookMemo[i])
        file.write(data)
    file.close()

    return render_template(BOOKDATA_HTML, title = bookTitle, publisher = bookPublisher, writer = bookWriter, len = bookLength, memo = bookMemo)

if __name__ == '__main__': # 실행
        app.run(host='0.0.0.0', port=8080, debug=True)
