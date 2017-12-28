import psycopg2


def conexion(b, h, u, p):
    try:
        conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (b,u,h,p))
        return conn.cursor()
    except ValueError:
        print("Ocurrio un error al conectar a la base de datos.")
    
