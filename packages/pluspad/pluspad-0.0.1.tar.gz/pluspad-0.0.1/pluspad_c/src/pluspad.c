#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* Function doing the work */
static PyObject *
test_string(PyObject *self, PyObject *args)
{
    const char *string;

    if (!PyArg_ParseTuple(args, "s", &string))
    {
        return NULL;
    }
    
    printf("%s!\n", string);

    Py_RETURN_NONE;
}

/* Defining the module functions */
static PyMethodDef TestMethods[] = {
    {"test", test_string, METH_VARARGS, "Testing python C function."},
    {NULL, NULL, 0, NULL}
};

/* Defining the module */
static struct PyModuleDef pluspad_c =
{
    PyModuleDef_HEAD_INIT,
    "pluspad_c",    /* name of module */
    "",             /* module documentation, may be NULL */
    -1,             /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    TestMethods
};

/* Initiating it for the python interpreter */
PyMODINIT_FUNC PyInit_pluspad_c(void)
{
    return PyModule_Create(&pluspad_c);
}
