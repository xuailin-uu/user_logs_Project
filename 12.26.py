from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta
import mysql.connector
import datetime
import xlsxwriter
from flask import Flask, render_template, request, jsonify,send_from_directory
import pymysql

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:111@localhost/sqoopTest'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

def connect_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='111',
        database='sqoopTest'
    )
    return conn
# 表模板
class adsUvCountMysql(db.Model):
    __tablename__='ads_uv_count_mysql'
    dt=db.Column(db.String,primary_key=True)
    day_count=db.Column(db.Integer)
    wk_count=db.Column(db.Integer)
    mn_count=db.Column(db.Integer)
    is_weekend=db.Column(db.String)
    is_monthend=db.Column(db.String)
    def __str__(self):
        return "dt:{},day_count:{}".format(self.dt,self.day_count)

# 获取月份的总用户数量
def getMonthData(month):
    s='2022-%d-%%' % month
    data=db.session.query(adsUvCountMysql.dt,adsUvCountMysql.day_count).filter(adsUvCountMysql.dt.like(s)).all()
    num=sum([x.day_count for x in data])
    print(s)
    print(num)
    return [str(month),num]


def getYearData(year):
    s='%d-%%-%%' % year
    data=db.session.query(adsUvCountMysql.dt,adsUvCountMysql.day_count).filter(adsUvCountMysql.dt.like(s)).all()
    print(data)
    num=sum([x.day_count for x in data])
    print(s)
    print(num)
    return [str(year),num]

# 配置路由
@app.route("/", methods=['GET', 'POST'])
def index():
    # 获取四月的用户数量
    mouth_11=getMonthData(11)
    mouth_12=getMonthData(12)
    mouth_11_2023=getMonthData1(11)
    mouth_12_2023=getMonthData1(12)
    year_2022=getYearData(2022)
    year_2023=getYearData(2023)
    # 获取四月到五月每天的用户数量
    #dateRangeData1 = getMonthRange()
    # 获取四月到五月每周的用户数量
    #dateRangeData2 = getWeekRange()
    allData=db.session.query(adsUvCountMysql).all()
    if request.method == 'POST':
        result = query_data()
    else:result=[]

    data1={
        "keys3": [1,2,3,4,5,6,7,8,9,10,mouth_11[0],mouth_12[0]],
        "values3": [0,0,0,0,0,0,0,0,0,0,mouth_11[1],mouth_12[1]],
        "keys5": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, mouth_11_2023[0],  mouth_12_2023[0]],
        "values5": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, mouth_11_2023[1],  mouth_12_2023[1]],
        "keys4": [year_2022[0],year_2023[0]],
        "values4": [year_2022[1],year_2023[1]],

        "allData":allData,
        "result":result
    }
    # if request.method == 'POST':
    #     # data = query_data()
    #     return render_template('index.html', **data1)
    # else:
    return render_template('index.html',**data1)


def query_data():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM ads_uv_count_mysql WHERE dt LIKE '2023%'"
    # 执行查询语句
    cursor.execute(sql)
    result = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    return result

if __name__ =="__main__":
    app.run(debug=True)