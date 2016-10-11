from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
engine = create_engine('postgresql://read_only:User_ro@192.168.7.8:5432/Cubo')
meta = MetaData()
user_table = Table('vipproject', meta, autoload=True, autoload_with=engine)
[c.name for c in user_table.columns]
s = select([user_table.c.projectid,user_table.c.statisticlogin,user_table.c.statisticpassword]).where(user_table.c.domain == 'krovatky.ru')
p = []
for row in engine.execute(s):
    p.append(row)