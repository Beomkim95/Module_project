# 데이터베이스 연결
import pymysql

conn = pymysql.connect(host='172.17.0.3', user='root', password='', port=3306, db='mydb', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor) 

# 날짜 형식 
import datetime
now = datetime.datetime.today()

# 로그인 형식
def login_m():
    l_id = input('id를 입력하세요 : ')
    l_pwd = input('pwd를 입력하세요 : ')
    
    if l_id == 'admin' and l_pwd == 'admin123' :
        print('로그인이 성공하였습니다')
    else :
        print("로그인에 실패하였습니다.")
        main()

def login():
    l_email = input('이메일을 입력하세요 : ')
    l_pwd = input('pwd를 입력하세요 : ')

    logsql = "SELECT pwd , email FROM Member WHERE email = '{0}'".format(l_email)
    cursor.execute(logsql)
    result = cursor.fetchall()
    for row in result :
        if l_email == row['email'] :
            if l_pwd == row['pwd'] :
                print('로그인이 성공하였습니다')

            else :
                print("로그인에 실패하였습니다.")
                main()
        else :
            print("로그인에 실패하였습니다.")
            main()

# 전체 회원목록 조회
def displayMember():
    sql4 = "SELECT * FROM Member"
    cursor.execute(sql4)
    rows = cursor.fetchall()
    for row in rows:
        print('번호:{0}, 이메일:{1}, 비밀번호:{2}, 가입날짜:{3}'.format(row['id'], row['email'],row['pwd'], row['created_at']))

# 개인 회원정보 조회
def personmember():
    p_email = input("본인의 이메일을 입력하세요 : ")
    persql = "SELECT * FROM Member where email = '{0}'".format(p_email)
    cursor.execute(persql)
    rows = cursor.fetchall()
    for row in rows:
        print('번호:{0}, 이메일:{1}, 비밀번호:{2}, 가입날짜:{3}'.format(row['id'], row['email'],row['pwd'], row['created_at']))    

# 개인 회원정보 수정
def re_member():
    print("개인 회원정보 수정입니다!")
    real_id = input('회원의 번호(id)를 입력하세요 : ')
    re_em = input('원하는 이메일을 입력하세요 : ')
    re_pwd = input('원하는 비밀번호를 입력하세요 : ')
    
    updatesql1 = "UPDATE Member SET email= '{}' WHERE id = '{}'".format(re_em,real_id)
    updatesql2 = "UPDATE Member SET pwd = '{}' WHERE id = '{}'".format(re_pwd,real_id)

    cursor.execute(updatesql1)
    cursor.execute(updatesql2)
    conn.commit()
    print("개인정보 수정이 완료되었습니다.")

# 전체 주문목록 조회
def searchorder():
    sql = "SELECT * FROM Order_"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print('번호:{0}, 회원이름:{1}, 상품이름:{2}, 주문수량:{3}, 총금액:{4}, 주문날짜:{5}'.format(row['id'], row['member_id'],  row['item_id'], row['order_qty'], row['order_price'], row['created_at']))

# 회원탈퇴
def deletemember() :
    print("※ 회원 삭제는 비밀번호를 통해서 가능합니다.")
    dd_email = input("본인의 이메일을 입력해주세요 : ")
    d_pwd = input("본인의 비밀번호를 입력해주세요 : ")

    logsql = "SELECT pwd , email FROM Member WHERE email = '{0}'".format(dd_email)
    cursor.execute(logsql)
    result2 = cursor.fetchall()

    for row in result2 :
        if d_pwd == row['pwd'] :
            sql = 'DELETE FROM Member WHERE pwd = {0}'.format(d_pwd)
            cursor.execute(sql)
            conn.commit()
            print("회원 삭제가 완료되었습니다.")
            quit()
        
        else :
            print("비밀번호가 맞지 않습니다.") 

"""
    sql = 'DELETE FROM Member WHERE pwd = {0}'.format(d_pwd)
    cursor.execute(sql)
    conn.commit()
"""


# 상품목록에 상품추가
def additem() :
    p_name = input("상품이름 : ")
    p_price = float(input("가격 : "))
    p_qty = int(input("수량 : "))
    
    itemsql = "INSERT INTO item(p_name,p_price,p_qty,created_at) VALUES('{}','{}','{}','{}')".format(p_name, p_price, p_qty, now)
    cursor.execute(itemsql)
    conn.commit()
    print("상품목록에 상품입력이 완료되었습니다.")

# 상품목록 조회
def itemsearch():
    itemsql = "SELECT * FROM item"
    cursor.execute(itemsql)
    itrows = cursor.fetchall()
    for itrow in itrows:
        print('번호:{0}, 물건이름:{1}, 가격:{2}, 수량:{3}, 추가된날짜:{4}'.format(itrow['id'], itrow['p_name'],itrow['p_price'],itrow['p_qty'],itrow['created_at']))


# 상품 존재 유무

def checkitem():
    che_item = input("주문하고자 하는 상품을 입력하세요 : ")
    chsql = "SELECT p_qty FROM item where p_name = '{}'".format(che_item)
    cursor.execute(chsql)
    chrows = cursor.fetchall()
    for chrow in chrows:
        if chrow['p_qty'] > 0 :
            orderitem()
        else :
            print("재고가 부족합니다")

# 주문하기 
def orderitem() :
    ordermember = input("본인의 이메일 : ")
    orderit = input("물건 이름 : ")
    orderqty = int(input("주문할 수량 : "))
    orderpri = float(input("주문할 상품의 단위당 가격 : "))
    total = orderqty * orderpri


    ordersql = "INSERT INTO Order_(member_id,item_id,order_qty,order_price,created_At) VALUES('{}','{}','{}','{}','{}')".format(ordermember,orderit, orderqty, total, now)
    cursor.execute(ordersql)
    conn.commit()
    print("주문이 완료되었습니다.")  

    updatesql = "UPDATE item set p_qty = p_qty - %s WHERE p_name = %s "
    cursor.execute(updatesql,(orderqty,orderit))
    conn.commit()
    
# 주문취소
def deleteorder() :
    print("※ 주문취소는 이메일을 통해 가능합니다.")
    d_email = input("본인의 이메일를 입력해주세요 : ")
    sql = "DELETE FROM Order_ WHERE member_id = '{0}'".format(d_email)
    cursor.execute(sql)
    conn.commit()

# 주문한 상품 조회
def checkorder() :
    print("주문한 물건 목록입니다! ")
    c_email = input("본인의 이메일을 입력하세요 : ")
    c_sql = "SELECT * FROM Order_ WHERE member_id = '{0}'".format(c_email)
    cursor.execute(c_sql)
    c_rows = cursor.fetchall()
    for row in c_rows:
        print('번호:{0}, 이메일:{1}, 상품이름:{2}, 주문수량:{3}, 총가격{4}, 주문날짜{5}'.format(row['id'], row['member_id'],row['item_id'],row['order_qty'],row['order_price'],row['created_at']))

# 가장 많은 금액을 주문한 사용자 
def maxuser1() :
    maxus1 = "SELECT member_id FROM Order_ where order_price = (SELECT max(order_price) FROM Order_ )"
    cursor.execute(maxus1)
    conn.commit()
    print("검색이 완료되었습니다.")
    rows = cursor.fetchall()
    for row in rows:
        print('가장 많은 금액을 주문한 사용자 이메일 : {0}'.format(row['member_id']))
"""
def maxuser2() :
    maxus2 = "SELECT member_id FROM Order_ where order_price = (SELECT max(order_price) FROM Order_ groupy by week(created_at)) group by week(created_at) "
    cursor.execute(maxus2)
    conn.commit()
    print("검색이 완료되었습니다.")
    rows = cursor.fetchall()
    for row in rows:
        print('사용자 이메일:{0}'.format(row['member_id']))
"""

# 가장 많이 주문된 상품
def maxitem1() :
    maxsql1 = "SELECT item_id FROM Order_ where order_qty = (SELECT max(order_qty) FROM Order_ )"
    cursor.execute(maxsql1)
    conn.commit()
    print("검색이 완료되었습니다.")
    rows = cursor.fetchall()
    for row in rows:
        print('가장 많이 주문된 상품 : {0}'.format(row['item_id']))

"""
def maxitem2() :
    maxsql2 = "SELECT item_id FROM Order_ where order_qty = (SELECT max(order_qty) FROM Order_ group by month(created_at) group by month(created_at)) "
    cursor.execute(maxsql2)
    conn.commit()
    print("검색이 완료되었습니다.")
    rows = cursor.fetchall()
    for row in rows:
        print('상품:{0}'.format(row['item_id']))
"""

def main():
    print('#' * 50)
    print('#' * 10 + '쇼핑 프로그램입니다 ' + '#' * 20)
    print('#' * 50)
    print('# 1. 회원 로그인')
    print('# 2. 관리자 로그인')
    print('# 3. 회원 가입')
    print('# 4. 종료')
    print('번호를 선택하세요')
    print('#' * 50)
    print('#' * 50)
    print('#' * 50)

    while True:
        try:
            cmd = int(input('(1.회원 로그인 2.관리자 로그인 3.회원 가입 4. 종료 ) ->  '))

        except ValueError:
            print('1 ~ 4 사이의 명령어를 선택해 주세요.')
            continue
     
        if cmd == 2 :
            login_m()

            while True:
                try:
                    print('#' * 50)
                    print('1) 회원목록 조회')
                    print('2) 주문목록 조회')
                    print('3) 상품목록 조회')
                    print('4) 상품목록에 상품 추가 ')
                    print('5) 가장 많은 금액을 주문한 사용자 찾기')
                    print('6) 가장 많이 주문된 상품 찾기')
                    print('7) 시스템 종료')
                    cmd2 = int(input(' (1 ~ 7) -> '))
                    print('#' * 50)

                except ValueError:
                    print('1~7 사이의 명령어를 선택해 주세요.')
                    continue
        
                if cmd2 == 1:
                    print("1) 회원목록 조회 입니다")
                    displayMember()        

                elif cmd2 == 2:
                    print("2) 주문목록 조회 입니다.")
                    searchorder()

                elif cmd2 == 3:
                    print("3) 상품목록 조회 입니다.")
                    itemsearch()

                elif cmd2 == 4:
                    print("4) 상품목록에 상품 추가 입니다.")
                    additem()

                elif cmd2 == 5:
                    print("5) 가장 많은 금액을 사용한 사용자 찾기입니다.")
                    maxuser1()

                elif cmd2 == 6:
                    print("6) 가장 많이 주문된 상품 찾기입니다.")
                    maxitem1()
                    """
                    cri2 = input("무엇을 기준으로 하겠습니까? 1)주 2)월 : ")
                    if cri2 == 1 :
                        maxitem1()
                    else :
                        maxitem2()
                    """

                elif cmd2 == 7:
                    cursor.close()
                    conn.close()
                    quit()
                else:
                    print("잘못 된 명령어 입니다. 다시 입력해 주세요.")
                    continue

        elif cmd == 1 :
            login()

            while True:
                try:
                    print('#' * 50)
                    print('1) 회원정보 확인')
                    print('2) 회원정보 수정')
                    print('3) 회원탈퇴')
                    print('4) 상품주문')
                    print('5) 주문목록 확인')
                    print('6) 주문취소')
                    print('7) 시스템 종료')
                    cmd3 = int(input(' (1~7) -> '))
                    print('#' * 50)
                except ValueError:
                    print('1~7 사이의 명령어를 선택해 주세요.')
                    continue
        
                if cmd3 == 2:
                    print("1) 회원정보 수정입니다")
                    re_member()

                elif cmd3 == 1:
                    print("2) 회원정보 확인입니다")    
                    personmember() 

                elif cmd3 == 3:
                    print("3) 회원탈퇴 입니다.")
                    deletemember()
                    quit()

                elif cmd3 == 4:
                    print("4) 상품주문 입니다.")
                    itemsearch()
                    checkitem()

                elif cmd3 == 5:
                    print("5) 주문목록 확인입니다.")
                    checkorder()

                elif cmd3 == 6:
                    print("6) 주문취소 입니다.")
                    deleteorder()

                elif cmd3 == 7:
                    cursor.close()
                    conn.close()
                    quit()
                else:
                    print("잘못된 명령어 입니다. 다시 입력해 주세요.")
                    continue

        elif cmd == 3 :
            email = input("email : ")
            pwd = input("pwd : ")
            insertsql = "INSERT INTO Member(email,pwd,created_at) VALUES('{}','{}','{}')".format(email, pwd, now)
            cursor.execute(insertsql)
            conn.commit()
            print("회원가입이 완료되었습니다.")
            
        else :
            print("프로그램을 종료합니다. ")
            break

main()
