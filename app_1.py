from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)
# 连接数据库
def connect_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='111',
        database='sqoopTest'
    )
    return conn
# 查询数据库中 dt 字段满足条件的数据
def query_data():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM ads_uv_count_mysql WHERE dt LIKE '2022%'"
    # 执行查询语句
    cursor.execute(sql)
    result = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理按钮点击事件
        data = query_data()
        return render_template('index1.html', data=data)
    else:
        return render_template('index1.html')
if __name__ == '__main__':
    app.run(debug=True)