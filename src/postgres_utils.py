import psycopg2

# try:
#     cur = conn.cursor()

#     try:
#         cur.execute( """INSERT INTO items (name, description) 
#                       VALUES (%s, %s)  RETURNING id""", (item[0], item[1]))
#     except psycopg2.IntegrityError:
#         conn.rollback()
#     else:
#         conn.commit()

#     cur.close() 
# except Exception , e:
#     print 'ERROR:', e[0]
