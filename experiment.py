import pyarrow
t = pyarrow.Table.from_pydict({"fruit": ["apple", "apple", "banana", "orange"], "price": [0.5, 0.5, 0.25, 0.33]})

import ibis
import ibis.expr.schema as sch
import ibis.backends.pyarrow.datatypes
table_schema = sch.schema(t.schema)

import ibis.expr.sql
x = ibis.expr.sql.parse_sql("SELECT price FROM fruits WHERE fruit='banana'", catalog={"fruits": table_schema})

from ibis_substrait.compiler.core import SubstraitCompiler
compiler = SubstraitCompiler()
plan = compiler.compile(x)

import pyarrow.substrait
r = pyarrow.substrait.run_query(pyarrow.py_buffer(plan.SerializeToString()), table_provider=lambda *args: t)

print(r.read_all())
