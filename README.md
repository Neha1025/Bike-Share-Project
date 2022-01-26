Your task is to create a software system to support a bike share programme (like NextBike in Glasgow, or Santander Cycles in London). You need to create a functioning end-to-end prototype and demonstrate it with appropriate data. Your product is meant to provide an interface for customers to reserve and return bikes and to pay their bills; for operators to assess the state of the system and make changes if necessary; and for managers to view usage reports.


# User Manual of 1l team project

## test method of the project

Switch directory to the project, and run code below:

``` bash
python3 -m unittest test_backend.TestCostmers -v
```

If it meets the design requirements, it will be output as shown below

![run_costmers_test](./pic/pic1_run_costmers_test.png)

 `test_backend.TestCostmers`

Above part of the command can be change to

 `test_backend.TestOperators`

or

 `test_backend.TestManagers`

 to test corresponding role.

Can also use below command to run all test.

``` bash
python3 -m unittest test_backend.py -v
```
