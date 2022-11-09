import hashlib
from hashlib import md5
from base64 import b64decode, b16encode
from ldap3 import Server, Connection, ALL


def autenticacion_ldap(username, password):
    server = Server('host.docker.internal',  get_info=ALL)
    username = str(username)
    password = str(password)
    conn = Connection(server, 'cn=admin,dc=sia,dc=unal,dc=edu,dc=co', 'admin', auto_bind=True)
    #print(conn.extend.standard.who_am_i())
    #print(conn)
    #print(conn.bound)
    #print(conn.search('dc=sia,dc=unal,dc=edu,dc=co', '(objectclass=person)'))
    #print(conn.start_tls())
    conn.search('dc=sia,dc=unal,dc=edu,dc=co', '(&(objectclass=person)(cn='+username+'))', attributes=['sn', 'givenName', 'objectclass','userPassword'])
    clave = conn.entries
    calve_encriptada = str(clave[0]['userPassword'])
    a = calve_encriptada.split('}')
    b = a[1].split("\'")
    #print(b[0])
    z = str(b16encode(b64decode(b[0])).lower())
    z = z.split("\'")
    #print(z[1], 'nuevo intento')
    #print(md5(password.encode('utf-8')).digest(), 'esta es una prueba')
    password_encode = password.encode('utf-8')
    #print(hashlib.md5(z.encode('utf-8')).hexdigest(), 'prueba')
    d = md5(password_encode).hexdigest()
    print(d , 'comparación')

    if d == z[1]:
        return 'Ldap login correcto'
    
