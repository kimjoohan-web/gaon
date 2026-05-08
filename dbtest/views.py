from django.shortcuts import render
import pyodbc
from django.core.paginator import Paginator 
# Create your views here.

#mssql 연동 테스트용 뷰입니다.

msconnect = {
    'host': 'wws12-002.cafe24.com',
    'port': '1433',
    'user':'nicejoodding',
    'password':'fdkwon8824@',
    'database':'nicejoodding',
    'driver':'ODBC Driver 17 for SQL Server',
    
}

connstr = f"DRIVER={msconnect['driver']};SERVER={msconnect['host']},{msconnect['port']};DATABASE={msconnect['database']};UID={msconnect['user']};PWD={msconnect['password']}"


def dbtest(request):
    # DB 연결 테스트 코드 작성
    
        page = request.GET.get('page', '1')  # 페이지    
        kw = request.GET.get('kw','')  

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        sql = "select top 100 * from Event_Member order by  mem_idx desc"        
        cursor.execute(sql)
        row = cursor.fetchall()
       
        paginator = Paginator(row, 10)  # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)
        
        context ={'d_list':page_obj,'page':page,'kw':kw,}    
        
    
        return render(request, 'dbtest/dbtest.html', context)

def db_create(request):
    pass

def db_detail(request, dbtest_id):
    pass   