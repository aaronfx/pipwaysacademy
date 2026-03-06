2026-03-06T13:06:16.958335585Z   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
2026-03-06T13:06:16.958337825Z   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
2026-03-06T13:06:16.958339915Z   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
2026-03-06T13:06:16.958341985Z   File "/opt/render/project/src/run.py", line 3, in <module>
2026-03-06T13:06:16.958356636Z     app = create_app()
2026-03-06T13:06:16.958358976Z   File "/opt/render/project/src/app/__init__.py", line 33, in create_app
2026-03-06T13:06:16.958361076Z     db.create_all()
2026-03-06T13:06:16.958363106Z     ~~~~~~~~~~~~~^^
2026-03-06T13:06:16.958365206Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask_sqlalchemy/extension.py", line 900, in create_all
2026-03-06T13:06:16.958367386Z     self._call_for_binds(bind_key, "create_all")
2026-03-06T13:06:16.958369486Z     ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-06T13:06:16.958371576Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask_sqlalchemy/extension.py", line 881, in _call_for_binds
2026-03-06T13:06:16.958373616Z     getattr(metadata, op_name)(bind=engine)
2026-03-06T13:06:16.958375686Z     ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
2026-03-06T13:06:16.958377736Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/schema.py", line 5928, in create_all
2026-03-06T13:06:16.958379836Z     bind._run_ddl_visitor(
2026-03-06T13:06:16.958381916Z     ~~~~~~~~~~~~~~~~~~~~~^
2026-03-06T13:06:16.958384096Z         ddl.SchemaGenerator, self, checkfirst=checkfirst, tables=tables
2026-03-06T13:06:16.958386156Z         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-06T13:06:16.958388237Z     )
2026-03-06T13:06:16.958390387Z     ^
2026-03-06T13:06:16.958392497Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 3268, in _run_ddl_visitor
2026-03-06T13:06:16.958394577Z     conn._run_ddl_visitor(visitorcallable, element, **kwargs)
2026-03-06T13:06:16.958396657Z     ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-06T13:06:16.958398777Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2467, in _run_ddl_visitor
2026-03-06T13:06:16.958400877Z     ).traverse_single(element)
2026-03-06T13:06:16.958402907Z       ~~~~~~~~~~~~~~~^^^^^^^^^
2026-03-06T13:06:16.958404997Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/visitors.py", line 661, in traverse_single
2026-03-06T13:06:16.958407087Z     return meth(obj, **kw)
2026-03-06T13:06:16.958417667Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/ddl.py", line 962, in visit_metadata
2026-03-06T13:06:16.958419997Z     collection = sort_tables_and_constraints(
2026-03-06T13:06:16.958422097Z         [t for t in tables if self._can_create_table(t)]
2026-03-06T13:06:16.958424217Z     )
2026-03-06T13:06:16.958427008Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/ddl.py", line 1394, in sort_tables_and_constraints
2026-03-06T13:06:16.958429108Z     dependent_on = fkc.referred_table
2026-03-06T13:06:16.958431158Z                    ^^^^^^^^^^^^^^^^^^
2026-03-06T13:06:16.958433338Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/schema.py", line 4799, in referred_table
2026-03-06T13:06:16.958435408Z     return self.elements[0].column.table
2026-03-06T13:06:16.958437458Z            ^^^^^^^^^^^^^^^^^^^^^^^
2026-03-06T13:06:16.958439508Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/util/langhelpers.py", line 1123, in __get__
2026-03-06T13:06:16.958441688Z     obj.__dict__[self.__name__] = result = self.fget(obj)
2026-03-06T13:06:16.958443728Z                                            ~~~~~~~~~^^^^^
2026-03-06T13:06:16.958445808Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/schema.py", line 3199, in column
2026-03-06T13:06:16.958447898Z     return self._resolve_column()
2026-03-06T13:06:16.958454038Z            ~~~~~~~~~~~~~~~~~~~~^^
2026-03-06T13:06:16.958456178Z   File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/schema.py", line 3222, in _resolve_column
2026-03-06T13:06:16.958458218Z     raise exc.NoReferencedTableError(
2026-03-06T13:06:16.958460298Z     ...<5 lines>...
2026-03-06T13:06:16.958462429Z     )
2026-03-06T13:06:16.958466269Z sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'courses.instructor_id' could not find table 'users' with which to generate a foreign key to target column 'id'
