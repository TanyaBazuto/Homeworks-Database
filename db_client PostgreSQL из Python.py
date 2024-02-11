import psycopg2

#Функция, создающая структуру БД (таблицы).
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL,
            email VARCHAR(40) NOT NULL UNIQUE
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(client_id) ON DELETE CASCADE,
            phone VARCHAR(20) UNIQUE 
        );
        ''')

#Функция, удаляющая БД (таблицы).
def delete_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE phone_number;
        DROP TABLE client;
        ''')

#Функция, позволяющая добавить нового клиента
def add_client(conn, first_name: str, last_name: str, email: str, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO client(first_name, last_name, email)
        VALUES(%s, %s, %s) RETURNING client_id, first_name, last_name, email;
        ''', (first_name, last_name, email))
        return cur.fetchone()

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id: str, phone: str):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phone_number(client_id, phone)
        VALUES(%s, %s) RETURNING id, client_id, phone;
        ''', (client_id, phone))
        return cur.fetchone()

#Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE client SET client_id=%s, first_name=%s, last_name=%s, email=%s
        RETURNING client_id, first_name, last_name, email;
        ''', (client_id, first_name, last_name, email))
        return cur.fetchall()

#Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, id, client_id=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM phone_number WHERE id=%s
        RETURNING id, client_id, phone;
        ''', (id,))
        return cur.fetchone()

#Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM client WHERE client_id=%s
        RETURNING client_id, first_name, last_name;
        ''', (client_id,))
        return cur.fetchone()

#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM client cl
        LEFT JOIN phone_number ph ON cl.client_id = ph.client_id
        WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
        AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
        AND (email = %(email)s OR %(email)s IS NULL)
        OR (phone = %(phone)s OR %(phone)s IS NULL);
        ''', {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})
        return cur.fetchone()


if __name__ == '__main__':
    with psycopg2.connect(database = 'netology_db', user = 'postgres', password = '********') as conn:
        with conn.cursor() as cur:
            print(delete_db(conn))
            print(create_db(conn))
            print(add_client(conn, first_name='Tatyana', last_name='Bazuto', email='bazuto@mail.ru'))
            print(add_phone(conn, client_id=1, phone='8912508053'))
            print(add_phone(conn, client_id=1, phone='8912542938'))
            print(change_client(conn, client_id=1, first_name='Tatyana', last_name='Solonik', email='bazuto@mail.ru'))
            print(delete_phone(conn, id=2))
            # print(delete_client(conn, client_id=1))
            print(find_client(conn, first_name='Tatyana'))


conn.close()
