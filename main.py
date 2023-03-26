from flask import Flask, render_template, request
import pymysql
import markdown

app = Flask(__name__, template_folder='static')


@app.template_filter('render_markdown')
def render_markdown(text):
    # 将 &nbsp; 替换为空格
    text = text.replace('&nbsp;', ' ')
    # 将连续的空格和换行符替换为 <br> 标签
    text = text.replace('  ', ' &#160;').replace('\n', '<br>')
    # 将长代码块用 <pre><code> 标签包裹起来，并添加 tab-size 属性
    text = text.replace('```', '<pre><code style="tab-size: 4">').replace('```', '</code></pre>')
    return markdown.markdown(text)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search_button' in request.form:
            query = request.form['search_text'].strip()
            if len(query) >= 2:
                results = search(query)
                return render_template('index.html', results=results)
        elif 'add_button' in request.form:
            id = request.form['id_text'].strip()
            text = request.form['text_text'].strip()
            if id and text:
                add(text, id)
                results = search(text)
                print(request)
                return render_template('index.html', results=results)
            else:
                add(text)
                results = search(text)
                print(request)
                return render_template('index.html', results=results)

        elif 'update_button' in request.form:
            id = request.form['id_text'].strip()
            text = request.form['text_text'].strip()
            if id and text:
                update(id, text)
                results = search(text)
                return render_template('index.html', results=results)
        elif 'delete_button' in request.form:
            id = request.form['id_text'].strip()
            if id:
                delete(id)
                return render_template('index.html')
        return render_template('index.html')
    else:
        return render_template('index.html')


def connect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='62387237',
        database='tgdb'
    )

    return connection


def search(query):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT id, text FROM message WHERE text LIKE %s", (f'%{query}%',))
        results = cursor.fetchall()
        connection.close()

        return results
    except Exception as e:
        print(e)


def add(text, id=None):
    try:
        connection = connect()
        cursor = connection.cursor()
        if id:
            # insert with specified id
            cursor.execute("INSERT INTO message (id, text) VALUES (%s, %s)", (id, text))
        else:
            # insert without specified id
            cursor.execute("INSERT INTO message (text) VALUES (%s)", (text,))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


def update(id, text):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE message SET text = %s WHERE id = %s", (text, id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


def delete(id):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM message WHERE id = %s", (id,))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True)
