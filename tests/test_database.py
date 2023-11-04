import csv
import config
import copy
import unittest
import database as db
import helpers



class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente("15J","Marta","Perez"),
            db.Cliente("47A","Carlos","Sosa"),
            db.Cliente("31F","Martin","Gomez"),
        ]
    
    def test_buscar_cliente(self):
        cliente_existente= db.Clientes.buscar("15J")
        cliente_inexistente= db.Clientes.buscar("99X")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_clientes(self):
        nuevo_cliente = db.Clientes.crear("32M","Juan","Pancho")
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni, "32M")
        self.assertEqual(nuevo_cliente.nombre, "Juan")
        self.assertEqual(nuevo_cliente.apellido, "Pancho")
    
    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar("31F"))
        cliente_modificado = db.Clientes.modificar("31F","Roberto","Carlos")
        self.assertEqual(cliente_a_modificar.nombre,"Martin")
        self.assertEqual(cliente_modificado.nombre,"Roberto")
        self.assertEqual(cliente_a_modificar.apellido,"Gomez")
        self.assertEqual(cliente_modificado.apellido,"Carlos")
    
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar("47A")
        cliente_rebuscado = db.Clientes.buscar("47A")
        self.assertEqual(cliente_borrado.dni,"47A")
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido("33A", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("asdasdasdas",db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("333",db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("47A",db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar("15J")
        db.Clientes.borrar("47A")
        db.Clientes.modificar("31F","Martin","Godoy")

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH,newline="\n") as fichero:
            reader = csv.reader(fichero,delimiter=";")
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni, "31F")
        self.assertEqual(nombre, "Martin")
        self.assertEqual(apellido, "Godoy")
        


        
