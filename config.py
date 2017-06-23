CLUSTERS = [
    {'address':'127.0.0.1', 'name':'local_cluster_1', 'port':'40001'},
    {'address':'127.0.0.1', 'name':'local_cluster_2', 'port':'40002'},
    {'address':'127.0.0.1', 'name':'local_cluster_3', 'port':'40003'},
    {'address':'127.0.0.1', 'name':'local_cluster_4', 'port':'40004'},
]

DATABASES = {
    'sqlite': [
        {'database_name': 'datastore/poll_1.db'},
        {'database_name': 'datastore/poll_2.db'},
        {'database_name': 'datastore/poll_3.db'},
        {'database_name': 'datastore/poll_4.db'},
        {'database_name': 'datastore/poll_5.db'},
        {'database_name': 'datastore/poll_6.db'},
        {'database_name': 'datastore/poll_7.db'},
        {'database_name': 'datastore/poll_8.db'},
        {'database_name': 'datastore/poll_9.db'},
        {'database_name': 'datastore/poll_10.db'}
    ]
}


POSTGRES_DATABASES = [
    {'database_name': 'test',
     'user': 'postgres',
     'password':'mysecretpassword',
     'host':'127.0.0.1',
     'port': 5432
    },
]

MYSQL_DATABASES = [
    {'database_name': 'employees',
     'user': 'root',
     'password':'mysecretpassword',
     'host':'127.0.0.1',
     'port': 3306
    },
]
