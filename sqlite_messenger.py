import sqlite3


def db_creator():
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE message (agent_from int, agent_to int, t_stamp real, data text, m_type text)''')
    # Insert a row of data
    #c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def send_message(mtype,afrom, ato, t_stamp ,data ):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''INSERT INTO message VALUES (?,?,?,?,?)''',(afrom, ato, t_stamp, data,mtype,))
    conn.commit()
    conn.close()

    return







def poll_for_incoming(polling_agent):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    # Do this instead
    #t = ('RHAT',)
    #c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    #print(c.fetchone())
    msg_list = []
    for row in c.execute('''SELECT * FROM message WHERE agent_to = ? ORDER BY message.t_stamp DESC ''', (polling_agent,)):
        print(row)
        msg_list.append(row)

    return msg_list


#send_message(1,2,3,'TEST')
poll_for_incoming(2)