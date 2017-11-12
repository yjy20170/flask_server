import pymysql

import warnings
warnings.filterwarnings("ignore")

class table():
    def __init__(self,tb='users',db='rf'):
        self.db=db#database name
        self.tb=tb#table name
        self.conn=pymysql.connect('localhost','root','',self.db)
        self.cursor=self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def do(self,string):#缩减代码
        self.cursor.execute(string)
    def show(self):
        self.do('select * from %s'%(self.tb))
        result=self.cursor.fetchall()
        if len(result)==0:
            print("the table '%s' is empty."%(self.tb))
        else:
            print("the table '%s' has %d rows:"%(self.tb,len(result)))
            for row in result:
                print(row)
    
class tableU(table):#U-users 用户id、姓名、密码、年龄、性别
    def append(self,name,password,age=60,sex=0):
        self.do("insert into %s(name,password,age,sex) value('%s','%s',%d,%d)"%(self.tb,name,password,age,sex))
        self.conn.commit()
    def delete(self,i):#仅供调试，实际中不会删除，保证每人的ID不变
        self.do('select MAX(id) from %s'%(self.tb))
        result=self.cursor.fetchone()[0]
        self.do('delete from {0} where id={1};update {0} set id=id-1 where id>{1};\
            ALTER TABLE {0} AUTO_INCREMENT = {2};'.format(self.tb,i,result))
        self.conn.commit()
    def checkLogin(self,name,pw):
        self.do("select * from %s where name='%s' and password='%s'"%(self.tb,name,pw))
        if len(self.cursor.fetchall())==0:
            return False
        return True


class tableD(table):#D-data 每个用户实时更新的数据
    def __init__(self,ID,db='rf'):
        self.max=300#记录数据的最大条数
        self.ID=ID#每个用户对应一ID
        self.db=db
        self.tb='d'+str(ID)
        self.conn=pymysql.connect('localhost','root','',self.db)
        self.cursor=self.conn.cursor()
        #若不存在，创建名为'd{}'.format(ID)的表
        self.do("create table if not exists d%d(id int(10) auto_increment,time float not null,\
            v int not null,primary key(id))ENGINE=InnoDB DEFAULT CHARSET=utf8;"%(ID))
    def delete(self,i):#delete(1)+append()可实现队列性质
        self.do('select MAX(id) from %s'%(self.tb))
        result=self.cursor.fetchone()[0]
        self.do('delete from {0} where id={1};update {0} set id=id-1 where id>{1};\
            ALTER TABLE {0} AUTO_INCREMENT = {2};'.format(self.tb,i,result))
        self.conn.commit()
    def append(self,time,v):#时间，心电，若条数达到self.max, 删除第一条
        self.do('select MAX(id) from %s'%(self.tb))
        result=self.cursor.fetchone()[0]
        if result>=self.max:
            self.do('delete from {0} where id={1};update {0} set id=id-1 where id>{1};\
            ALTER TABLE {0} AUTO_INCREMENT = {2};'.format(self.tb,1,result))
        self.do("insert into %s(time,v) value(%f,%d)"%(self.tb,time,v))
        self.conn.commit()
    def die(self):#仅供调试
        self.do('drop table %s'%(self.tb))
        self.conn.commit()

u=tableU()
def manage(name):
    if name in dic.keys():
        return dic[name]
    else:
        return 'ERROR'
if __name__=='__main__':
    u=tableU()
    u.show()
    d1=tableD(1)
    d1.show()
