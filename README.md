# dumdb
Experimental Dumb Database written in Ibis+Arrow+Substrait

## Try
Run:
```
$ python experiment.py "SELECT first_name,last_name,title FROM userdata1 WHERE country='Canada' LIMIT 5"
LOADING TABLE: userdata1.parquet

  first_name  last_name                        title
0     Albert    Freeman                Accountant IV
1    Deborah  Armstrong   Quality Control Specialist
2     Gloria   Hamilton     Systems Administrator IV
3      Aaron     Torres              Sales Associate
4      Peter    Russell  Computer Systems Analyst IV
```

or:
```
$ python experiment.py "SELECT gender, count(id) as count FROM userdata1 WHERE country='Canada' GROUP BY gender"
LOADING TABLE: userdata1.parquet

   gender  count
0    Male     12
1  Female      6
2              1
```
