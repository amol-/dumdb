import glob
import os
import argparse
import pyarrow
import pyarrow.parquet
import pyarrow.substrait
import ibis
import ibis.expr.schema as sch
import ibis.backends.pyarrow.datatypes
import ibis.expr.sql
from ibis_substrait.compiler.core import SubstraitCompiler

def main():
    parser = argparse.ArgumentParser(
        description = 'Run SQL queries on parquet files'
    )
    parser.add_argument(
        "query", 
        help="The query to run"
    )
    opts = parser.parse_args()
    
    # Detect all available Tables and their schemas
    catalog = {}
    for pqtfile in glob.glob("*.parquet"):
        table_name, _ = os.path.splitext(os.path.basename(pqtfile))
        table_schema = pyarrow.parquet.read_schema(pqtfile)
        catalog[table_name] = sch.schema(table_schema)
    print("CATALOG", list(catalog.keys()))

    # Parse the query to Substrait
    q = ibis.expr.sql.parse_sql(opts.query, catalog=catalog)
    compiler = SubstraitCompiler()
    plan = compiler.compile(q)

    # Run the query
    result = pyarrow.substrait.run_query(pyarrow.py_buffer(plan.SerializeToString()), 
                                         table_provider=table_provider)
    result_table = result.read_all()
    print(result_table.to_pandas())


def table_provider(table_name):
    filename = f"{table_name[0]}.parquet"
    print("LOADING TABLE", filename)
    table = pyarrow.parquet.read_table(filename)
    return table


if __name__ == "__main__":
    main()