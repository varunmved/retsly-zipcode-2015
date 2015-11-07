from utils.mysqlconn import MySQLDBConn

with MySQLDBConn() as db_conn:
    print("hello!")
    query = """
            create table foo (
                name    text,
                userid  int 
            )
            """
    db_conn.executeWriteQuery(query)

    query = """
            insert into foo (name, userid) values 
                ('chali', 12345),
                ('bennis', 21412),
                ('balloon', 471721)
            """
    n = db_conn.executeWriteQuery(query)
    print("inserted %s rows" % n)
    
    query = "select * from foo where userid >= %s" 
    fillers = (20000,)
    results = db_conn.executeReadQueryHash(query, fillers)
    print(results)

    query = "drop table foo"
    db_conn.executeWriteQuery(query)

