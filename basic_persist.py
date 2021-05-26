import psycopg2


def conectar():
    conn = psycopg2.connect(
        host="localhost",
        database="micrawl",
        user="postgres",
        password="roota")
    return conn


def save(data):
    sql = """INSERT INTO enlace(
	 url, estado, versiones, nombre, fecha)
	VALUES (%s, %s, %s, %s, %s);"""
    c = conectar()
    cursor = c.cursor()

    try:
        print(cursor.execute(sql, data))
        print(c.commit())
        cursor.close()
        c.close()

    except Exception as e:
        print("no se agrego " + str(data))
        print(e)
        pass


def leido(url):
    sql = """UPDATE public.enlace
	SET estado='leido'
	WHERE url=%s;"""
    c = conectar()
    cursor = c.cursor()

    try:
        print(cursor.execute(sql, url))
        print(c.commit())
        cursor.close()
        c.close()

    except Exception as e:
        print("no se edito " + str(url))
        print(e)
        pass
def obtenerEnlaces(leidos):
    sql = """SELECT * FROM enlace
    	WHERE estado='noleido';""" if leidos else "SELECT * FROM enlace;"
    c = conectar()
    cursor = c.cursor()

    data = []

    try:
        print(cursor.execute(sql))
        data = cursor.fetchall()
        cursor.close()
        c.close()

    except Exception as e:
        print("no se entrego enlaces ")
        print(e)
        pass

    return data


#save(("http2", "noleido", "3", "nombree","fecha"))

#leido(["http2"])

print(obtenerEnlaces(False))