#define PY_SSIZE_T_CLEAN
#include <Python.h>

uint64_t siphash(const uint8_t *in, const size_t inlen, const uint8_t *k);

static PyObject* pySiphash(PyObject* self, PyObject* args)
{
    PyBytesObject *data;
    PyBytesObject *seed;
    if (!PyArg_ParseTuple(args, "SS", &data, &seed))
        return NULL;
    if (PyBytes_Size((PyObject*)seed) != 16) {
        PyErr_SetString(PyExc_ValueError, "Seed length should be exactly 16 bytes");
        return NULL;
    }
    uint64_t hash = siphash(PyBytes_AsString((PyObject*)data), PyBytes_Size((PyObject*)data), PyBytes_AsString((PyObject*)seed));

    return PyLong_FromUnsignedLongLong(hash);
}

static PyMethodDef myMethods[] = {
    { "siphash", pySiphash, METH_VARARGS, "Calculate siphash" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "siphash",
    "Siphash calculation",
    -1,
    myMethods
};

PyMODINIT_FUNC PyInit_siphash(void)
{
    return PyModule_Create(&myModule);
}
