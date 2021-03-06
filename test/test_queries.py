import unittest
from mock import patch, MagicMock
from dorm.database.queries import DeleteQuery, UpdateQuery, SelectQuery
from dorm.database import models

class SelectQueryTestCase(unittest.TestCase):
    """ test select queries in here """

    @patch('dorm.database.drivers.base.BaseDriver')
    def setUp(self, BaseDriver):
        self.stub_model = MagicMock()
        self.stub_model.__tablename__ = "stub_model"
        dummy_conf = {'server_ip': '0.0.0.0', 'database_ip': '127.0.0.1', 'port': '0',
                      'type': 'test', 'database_name': 'test_db', 'user': 'test', 'password': 'test'}
        self.stub_model.__databases__ = [BaseDriver(dummy_conf), BaseDriver(dummy_conf)]

    def test_select_query_without_args(self):
        select_q = SelectQuery(self.stub_model)
        self.assertEqual('select * from stub_model;', select_q.sql)

    def test_select_query_with_args(self):
        select_q = SelectQuery(self.stub_model, 'id', 'name')
        self.assertEqual('select id, name from stub_model;', select_q.sql)

    def test_where_query(self):
        select_q = SelectQuery(self.stub_model, 'id', 'name')
        where_q = select_q.where(id=1)
        self.assertIsInstance(where_q, SelectQuery)
        self.assertEqual(
            'select id, name from stub_model where id=1;', select_q.sql)

    def test__base_function(self):
        select_q = SelectQuery(self.stub_model, 'name')
        select_q._base_function('foo')
        stub_db = select_q.databases[0]
        stub_db.execute.assert_called_with(
            commit=True, sql='select foo(name) from stub_model;')

    def test_avg(self):
        select_q = SelectQuery(self.stub_model, 'amount')
        stub_db = select_q.databases[0]
        select_q.avg()
        stub_db.execute.assert_called_with(
            commit=True, sql='select avg(amount) from stub_model;')

    def test_min(self):
        select_q = SelectQuery(self.stub_model, 'amount')
        stub_db = select_q.databases[0]
        select_q.min()
        stub_db.execute.assert_called_with(
            commit=True, sql='select min(amount) from stub_model;')

    def test_max(self):
        select_q = SelectQuery(self.stub_model, 'amount')
        stub_db = select_q.databases[0]
        select_q.max()
        stub_db.execute.assert_called_with(
            commit=True, sql='select max(amount) from stub_model;')

    def test_sum(self):
        select_q = SelectQuery(self.stub_model, 'amount')
        stub_db = select_q.databases[0]
        select_q.sum()
        stub_db.execute.assert_called_with(
            commit=True, sql='select sum(amount) from stub_model;')

    def test_count(self):
        select_q = SelectQuery(self.stub_model, 'amount')
        stub_db = select_q.databases[0]
        select_q.count()
        stub_db.execute.assert_called_with(
            commit=True, sql='select count(amount) from stub_model;')

    def test_first_without_datatype(self):
        select_q = SelectQuery(self.stub_model)
        select_q._execute = MagicMock(
            return_value=self.stub_model)  # check the return value
        select_q.first()
        select_q._execute.assert_called_with(
            'select * from stub_model limit 1;', datatype=None)

    def test_first_with_datatype(self):
        select_q = SelectQuery(self.stub_model)
        select_q._execute = MagicMock()  # check the return value
        select_q.first(datatype=dict)
        select_q._execute.assert_called_with(
            'select * from stub_model limit 1;', datatype=dict)

    def test_like(self):
        select_q = SelectQuery(self.stub_model, 'name')
        where_q = select_q.where(id=1)
        like_q = where_q.like('%mehmet%')  # check the invalid type
        self.assertIsInstance(where_q, SelectQuery)
        # query might be wrong
        self.assertEqual(
            'select name from stub_model where id=1 like %mehmet%;', select_q.sql)

    def test_all(self):
        select_q = SelectQuery(self.stub_model)
        select_q._execute = MagicMock(
            return_value=self.stub_model)  # check the return value
        select_q.all()
        select_q._execute.assert_called_with(
            'select * from stub_model;', batch_size=None, datatype=None)

    # this method is really important
    def test___getitem__with_one_slice(self):
        select_q = SelectQuery(self.stub_model)
        select_q._execute = MagicMock(
            return_value=self.stub_model)  # check the return value
        select_q[:1]
        select_q._execute.assert_called_with(
            'select * from stub_model limit 1 offset 0;', batch_size=None, datatype=None)

    # this method is really important, not done yet
    def test___getitem__with_two_slices(self):
        select_q = SelectQuery(self.stub_model)
        select_q._execute = MagicMock(
            return_value=self.stub_model)  # check the return value
        select_q[:1, :1]
        # select_q.databases[0]._execute.assert_called_with("hi")
        select_q._execute.assert_called_with(
            'select * from stub_model limit 1 offset 0;', batch_size=None, datatype=None)

    def test__make_instance_without_refered_fields(self):
        pass

    def test__execute(self):
        pass

class UpdateQueryTestCase(unittest.TestCase):
    """ test update queries in here """

    def setUp(self):
        self.stub_model = MagicMock()
        self.stub_model.__tablename__ = "stub_model"
        self.stub_model.__databases__ = []

    def test_update_query_with_without_update_fields(self):
        try:
            update_q = UpdateQuery(self.stub_model)
        except AssertionError as no_param_err:
            self.assertEqual(
                "Please define the fields you want to update. e.g update_fields=[{name:mehmet}]", no_param_err.args[0])

    def test_update_query_without_where_fields(self):
        try:
            update_q = UpdateQuery(self.stub_model, update_fields=[{'id': 1}])
        except AssertionError as no_param_err:
            self.assertEqual(
                "Please specify in which fields you want to update. e.g where_fields=[{id:1}]", no_param_err.args[0])

    def test_sql_property(self):
        update_fields = ({'name': 'test'})
        where_fields = ({'id': 1})
        update_q = UpdateQuery(
            self.stub_model, update_fields=update_fields, where_fields=where_fields)

        self.assertEqual(update_q.sql, update_q.base_sql.format(
            tablename=update_q.model.__tablename__, update_columns=' and '.join(update_q.update_list)))

    def test_update_query_with_kwargs_n_args(self):
        update_fields = ({'name': 'test'})
        where_fields = ({'id': 1})
        update_q = UpdateQuery(
            self.stub_model, update_fields=update_fields, where_fields=where_fields)
        self.assertEqual(
            'update stub_model set name=test where id=1;', update_q.sql)

    def test_set_method_changes_update_list_correctly(self):
        update_fields = ({'name': 'test'})
        where_fields = ({'id': 1})
        update_q = UpdateQuery(
            self.stub_model, update_fields=update_fields, where_fields=where_fields)

        update_q.set(age=24)
        self.assertEqual(
            'update stub_model set name=test and age=24 where id=1;', update_q.sql)

    def test_set_method_ignores_conflict(self):
        update_fields = ({'name': 'test'})
        where_fields = ({'id': 1})
        update_q = UpdateQuery(
            self.stub_model, update_fields=update_fields, where_fields=where_fields)

        update_q.set(name='test')
        self.assertEqual(
            'update stub_model set name=test where id=1;', update_q.sql)

    @patch('dorm.database.queries.db_job_spawner')
    def test_commit(self, job_spawner):
        update_fields = ({'name': 'test'})
        where_fields = ({'id': 1})
        update_q = UpdateQuery(
            self.stub_model, update_fields=update_fields, where_fields=where_fields)

        update_q.commit()
        job_spawner.assert_called_with(
            update_q.sql, self.stub_model.__databases__, commit=True)


class DeleteQueryTestCase(unittest.TestCase):
    """ test delete queries in here """

    def setUp(self):
        self.stub_model = MagicMock()
        self.stub_model.__tablename__ = "stub_model"
        self.stub_model.__databases__ = []

    def test_delete_query_without_args_n_kwargs(self):
        delete_q = DeleteQuery(self.stub_model)
        self.assertEqual('delete from stub_model;', delete_q.sql)

    def test_delete_query_with_args_without_kwargs(self):
        delete_q = DeleteQuery(self.stub_model, 'id=1')
        self.assertEqual('delete from stub_model where id=1;', delete_q.sql)

    def test_delete_query_with_kwargs_without_args(self):
        delete_q = DeleteQuery(self.stub_model, id=1)
        self.assertEqual('delete from stub_model where id=1;', delete_q.sql)

    def test_delete_query_with_kwargs_n_args(self):
        delete_q = DeleteQuery(self.stub_model, 'id=1', name='test')
        self.assertEqual(
            'delete from stub_model where id=1 and name=test;', delete_q.sql)

    @patch('dorm.database.queries.db_job_spawner')
    def test_commit(self, job_spawner):
        delete_q = DeleteQuery(self.stub_model, 'id=1', name='test')
        delete_q.commit()
        job_spawner.assert_called_with(
            delete_q.sql, self.stub_model.__databases__, commit=True)
