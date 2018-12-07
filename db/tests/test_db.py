"""Database and interface test functions. 

.. moduleauthor:: Mobile App Team

References
----------------
- mockupdb: https://emptysqua.re/blog/test-mongodb-failures-mockupdb/
- mockupdb: official: http://mockupdb.readthedocs.io/reference.html

"""

import unittest
import db.errors
import db.interface


class DbInterfaceTest(unittest.TestCase):
    """ Tests the functionality of the database interface functions. 
    
    .. seealso::
        Module :db.interface
    """

    def setUp(self):
        db.run_database(db.dbConfigType["memory"])

    def test_interface_exceptios(self):
        """Tests the exceptions of the database interface with invalid key value constellations.
        """
        @db.load("", "id")
        def test_with_key(self, a=None, b=None):
            pass

        @db.load("")
        def test_no_key(self, a=None, b=None):
            pass

        # test key value constellation
        with self.assertRaises(db.errors.DbInterfaceError):
            test_with_key(None, None)
        with self.assertRaises(db.errors.DbInterfaceError):
            test_no_key(None, 1)

    def test_interface(self):
        """Tests the save, load and delete functionality of the interface and the database.
        """

        ENTITY = "test"

        document = {"key": "value"}

        @db.save(ENTITY, "id")
        def test_save(self, model, object_id=None):
            return object_id

        @db.delete(ENTITY, "id")
        def test_delete(self, value, dbresult=None):
            return dbresult

        @db.load(ENTITY, "key")
        def test_load_with_key(self, value, dbresult=None):
            return dbresult

        @db.load(ENTITY)
        def test_load_no_key(self, dbresult=None):
            return dbresult


        # save tests-----------------------------------------------
        object_id = test_save(self, document)
        self.assertIsNotNone(object_id)

        # test insert same id
        #with self.assertRaises(pymongo.errors.DuplicateKeyError):
        #    test_save(self, {"_id": object_id})

        # test update
        object_id = test_save(self, {"id": object_id, "key": "value"})
        self.assertIsNotNone(object_id)

        # load tests-----------------------------------------------
        dbresult = test_load_with_key(self, "no_in_db")
        self.assertIsInstance(dbresult, list)
        self.assertIs(len(dbresult), 0)

        dbresult = test_load_with_key(self, "value")
        self.assertIsInstance(dbresult, list)
        self.assertEqual(dbresult[0]["key"], "value")

        dbresult = test_load_no_key(self)
        self.assertIsInstance(dbresult, list)
        self.assertGreater(len(dbresult), 0)

        # delete tests-----------------------------------------------
        result = test_delete(self, object_id)
        self.assertTrue(result)

        result = test_delete(self, object_id)
        self.assertFalse(result)

    def tearDown(self):
        pass
        #db.interface.database.client.drop_database(db.dbConfigType["memory"].DATABASE)


if __name__ == "__main__":
    unittest.main()