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
