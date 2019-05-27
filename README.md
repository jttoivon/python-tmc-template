# Using unit tests to automatically check Python exercises

## Libraries used

* For testing values: [unittest](https://docs.python.org/3/library/unittest.html)
* For testing how functions/methods have been called: [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
* NumPy utilities for testing: [numpy.testing](https://docs.scipy.org/doc/numpy/reference/routines.testing.html)
* Pandas utilities for testing: [pandas.testing](https://pandas.pydata.org/pandas-docs/stable/reference/general_utility_functions.html#testing-functions)

## Structure of the exercise folder

The model solution and students solution is in folder `src`.
The test driver is in folder `tmc`. The file `tmc/utils.py`
contains useful utilities. The unit tests are located in folder `test`.
All files in that folder whose name begins with ´test_` are inspected
for unit tests.

The files in the `src` folder are used to make both the model solution
and the exercise stub that is given to students.
The code that you don't want to include in the exercise stub
should be wrapped between `# BEGIN SOLUTION` and `# END SOLUTION`
lines. These lines may be indented. If students are requested
to write a function, then leave in the stub at least the
line that shows the function parameters. The solution
code between begin and end tags will be removed from the stub,
and possibly replaced with the code after the `# STUB:" tag,
if one exists.
If you want that a function should return a dictionary, you
can give a hint about this by adding the tag `# STUB: return {}`.

See the exercise `e00_example` for an example of using the tags
in the model solution.

### Test files

Usually you need just one test file, and that test file usually
uses only one test class. The test cases are the methods
of this test class. For the points a student can get by completing
an exercise I use the following coding: a point is a string with 
the following form `"pxx-yy.z"`, where `xx` is the part/week of the course,
yy is the exercise number in that week, and z is the point number.
I assume that xx, yy, and z are possibly zero padded integers.
If an exercise can only give one point, then give the following
decorator to the test **class**: `@points('pxx-yy.1')`.
If it is possible to get, for example three points from the exercise,
then use decorators  `@points('pxx-yy.1')`, `@points('pxx-yy.2')`,
and `@points('pxx-yy.3')`, in front of the test **cases**
that should be passed to get the corresponding point.

## Running tests

In an exercise folder (it should contain subfolders `src`, `tmc`, and
`test`) the command `python3 -m tmc` runs the tests. You can give the
option `-v` in the end for more verbose output.

## Check output

The helper function `get_out` (in file `tmc/utils.py`) returns
the printed output from the code executed in this test case. It returns
a string. A simple example follows:

```
    def test_output(self):
        main()
        out = get_out()  # what was printed while executing main
        self.assertEqual(out, "Hello, world!")
```

## Test a value

```
    def test_ret_val(self):
        ret_val = f()
        self.assertEqual(ret_val, 5, msg="Expected function f to return value 5!")
```

Note that when student runs `tmc test` and the test fails, he/she only
sees the values compared for the equality and the message given as the
`msg` argument. The stack trace is not shown to the student (it is visible in the TMC server, though). So, better make sure you always use the `msg`
argument and that it is informative enough.

Before checking the value, it may be informative to check that the type
of the return value is as expected:

```
    def test_ret_val(self):
        ret_val = f()
        self.assertEqual(type(ret_val), int, msg="Expected the return value to have type 'int'!")
        self.assertEqual(ret_val, 5, msg="Expected function f to return value 5!")
```

Due to limited precision of floating point numbers the operations
might sometimes return a slightly different value depending on
the implementation of computations. Therefore, equality testing
of floats should check only the first decimals. To
achive this use the `assertAlmostEqual` method and its `places` parameter.

```
    def test_ret_val(self):
        ret_val = f()
        self.assertEqual(type(ret_val), float, msg="Expected the return value to have type 'float'!")
        self.assertAlmostEqual(ret_val, 1.234567789, places=4, msg="Expected function f to return value 5!")
```

Use the most specific `assert` method so that the error message will be more
informative. For example, use `self.assertEqual(x, 5, msg="...")` instead of
`self.assertTrue(x==5, msg="...")`.

If testing a value inside some object, it is good to first check that
the value exists. Otherwise the error message maybe very confusing:

```
    def test_ret_val(self):
        ret_val = f()
        self.assertEqual(type(ret_val), list, msg="Expected the return value to have type 'list'!")
        self.assertGreaterEqual(len(ret_val), 1, msg="Expected that the returned list is non-empty!")
        self.assertEqual(type(ret_val[0]), int, msg="Expected the values in the returned list to have type 'int'!")
        self.assertEqual(ret_val[0], 5, msg="Expected function f to return value 5!")
```

In NumPy there are several integer types, such as: np.int8, np.int16, np.int32.
To check that a type is an integer type, use the below construct.
All the integer types are subdtypes of `np.integer`.

```
    def test_type(self):
        ret_val = f()
        self.assertTrue(np.issubdtype(ret_val, np.integer),
                        msg="Expected the return value to have integer type!")
```

NumPy and Pandas contain utilities for checking equality of arrays
and DataFrames:  [numpy.testing](https://docs.scipy.org/doc/numpy/reference/routines.testing.html) and [pandas.testing](https://pandas.pydata.org/pandas-docs/stable/reference/general_utility_functions.html#testing-functions).

## Check that a function or method is called

### Function calls

To check if a function or method was called and how it was called,
it needs to be *patched*. In the next example we check whether function `f`
calls, directly or indirectly, function `zip`.

```
    def test_calls(self):
        L1=[1,2,3]
        L2=[20,30,40]
        with patch("builtins.zip", wraps=zip) as pzip:
            result = f(L1, L2)
            pzip.assert_called()  # This does the same as the below test
	    self.assertGreaterEqual(pzip.call_count, 1, msg="Expected that function 'f' would call function 'zip'!")
```

To ensure that patching does not affect the normal operation of function `zip`,
we use the `wraps` parameter to tell that the patched function should
call the original function after it has recorded the call parameters.
Patching may not work for very primitive objects, like methods of lists.
And sometimes, even if it works, it may confuse the whole program.
It is not a good idea to patch some fundamental functions, like `int`.

The builtin functions are easy to patch, but functions in user importable
modules are harder to patch, because they can be imported and called in
several different ways. For example the NumPy function `np.linalg.inv`
can be imported and called in the following ways:
* import numpy; numpy.linalg.inv(m)
* from numpy import linalg; linalg.inv(m)
* from numpy.linalg import inv; inv(m)

The helper class `patch_helper` in file `tmc/utils.py` should
make patching possible in all these cases. First
create an object at the top-level: `ph = patch_helper(module_name)`.
Then in the test cases you use it like below:

```
    def test_called(self):
        a = np.array([[1,2], [3,4]])
        with patch(ph("np.linalg.inv"), wraps=np.linalg.inv) as pinv:
            p = f(a)
            pinv.assert_called()
```

The following example shows how to access the arguments to the calls of patched function.

```
    def test_called(self):
        with patch(ph("plt.scatter"), wraps=plt.scatter) as pscatter:
	     f()
	     pscatter.assert_called()
	     args, kwargs = pscatter.call_args[0]  # get the arguments of the first call to plt.scatter
	     self.assertEqual(len(args), 2, msg="Expected exactly two positional arguments to scatter!")
	     self.assertIn("label", kwargs, msg="Expected keyword argument 'label'!")
	     self.assertEqual(kwargs[label], "alpha", msg="Expected value 'alpha' to keyword argument 'label'!")
```

### Method calls


Patching a method of an object is done with the `patch.object` function.
Assume we want to patch the method `f` of an **instance** of class `A´:

```
class A(object):
    def f(self):
    	return 5
```

In the below example we patch the method `f` of an instance `a`:
```
    def test_calls(self):
        a = A()
        with patch.object(a, "f", wraps=a.f) as method_f:
	     g(a)
	     method_f.assert_called()

```

If we want to patch a method of all instances of a class, then the
original method cannot be simply wrapped using the `wraps` argument. To enable wrapping
we use the helper function `spy_decorator` from file `tmc/utils.py`.
Below is an example of this:

```
    def test_called(self):
        method_dropna = spy_decorator(pd.core.frame.DataFrame.dropna)
        with patch.object(pd.core.frame.DataFrame, "dropna", new=method_dropna):
            f()
            method_dropna.mock.assert_called()
```
