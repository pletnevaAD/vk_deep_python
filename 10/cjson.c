#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <Python.h>

PyObject* loads(PyObject* self, PyObject* args)
{
    PyObject *dict = NULL;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    char *json;
    if(!PyArg_ParseTuple(args, "s", &json))
    {
        printf("ERROR: Failed to parse arguments\n");
        return NULL;
    }
    while (isspace(*json)) {
        json++;
    }
    if (*json != '{') {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }
    json++;
    while (*json && *json != '}') {
        PyObject *key = NULL;
        PyObject *value = NULL;
        if (*json == ',') {
            json++;
        }
        while (isspace(*json)) {
            json++;
        }
        if (*json != '\"') {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
        json++;
        char *str_key = malloc(strlen(json) + 1);
        int i = 0;
        while (*json && *json != '\"'){
            str_key[i++] = *(json++);
        }
        if (*json != '\"') {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
        json++;
        str_key[i] = '\0';
        if (!(key = Py_BuildValue("s", str_key))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }
        while (isspace(*json)) {
            json++;
        }
        if (*json != ':') {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
        json+=1;
        while (isspace(*json)) {
            json++;
        }

        char *str_value = malloc(strlen(json) + 1);
        if (*json == '\"') {
            json++;
            int j = 0;
            while (*json && *json != '\"'){
                str_value[j++] = *(json++);
            }
            if (*json != '\"') {
                PyErr_Format(PyExc_TypeError, "Expected object or value");
                return NULL;
            }
            str_value[j] = '\0';
            json++;
            while (isspace(*json)) {
                json++;
            }

            if (!(value = Py_BuildValue("s", str_value))) {
                printf("ERROR: Failed to build string value\n");
                return NULL;
            }

        }
        else if (isdigit(*json) || *json == '-'){
            int j = 0;
            int dot = 0;
            int minus = 0;
            while (*json && (*json != ',') && (*json != '}')){
                str_value[j++] = *json;
                if (!isdigit(*json) && *json != '.' && *json!='-'){
                    printf("%s\n",json);
                    PyErr_Format(PyExc_TypeError, "Expected object or value");
                    return NULL;
                }
                if (*json == '.'){
                    if (dot>0){
                        PyErr_Format(PyExc_TypeError, "Expected object or value");
                        return NULL;
                    }
                    dot++;
                }
                if (*json == '-'){
                    if (minus>0){
                        PyErr_Format(PyExc_TypeError, "Expected object or value");
                        return NULL;
                    }
                    minus++;
                }
                json++;
            }
             if (*json != ',' && *json != '}') {
                PyErr_Format(PyExc_TypeError, "Expected object or value");
                return NULL;
            }
            str_value[j] = '\0';
            json++;
            while (isspace(*json)) {
                json++;
            }
            if (!(value = Py_BuildValue("f", atof(str_value)))) {
                printf("ERROR: Failed to build float value\n");
                return NULL;
            }
        }

        if (PyDict_SetItem(dict, key, value) < 0) {
            printf("ERROR: Failed to set item\n");
            return NULL;
        }

        Py_DECREF(key);
        Py_DECREF(value);
        free(str_key);
        free(str_value);
    }

    return dict;
}

PyObject* dumps(PyObject* self, PyObject* args)
{
    PyObject* my_dict;
    if (!PyArg_ParseTuple(args, "O", &my_dict)) {
        return NULL;
    }
    if (!PyDict_Check(my_dict)) {
        PyErr_Format(PyExc_TypeError, "Expected dict object");
        return NULL;
    }

    PyObject* keys = PyDict_Keys(my_dict);
    PyObject* values = PyDict_Values(my_dict);
    Py_ssize_t size = PyList_Size(keys);
    int total_size = 0;
    total_size += snprintf(NULL, 0, "{");
    char* buf = NULL;

    for (int i = 0; i < size; i++) {
        PyObject* key = PyList_GetItem(keys, i);
        PyObject* value = PyList_GetItem(values, i);

        PyObject* str_key = PyObject_Str(key);
        PyObject* str_value = PyObject_Str(value);
        const char* c_str_key = PyUnicode_AsUTF8(str_key);
        const char* c_str_value = PyUnicode_AsUTF8(str_value);

        if (PyNumber_Check(value)) {
            total_size += snprintf(NULL, 0, "\"%s\": %s", c_str_key, c_str_value);
        } else {
            total_size += snprintf(NULL, 0, "\"%s\": \"%s\"", c_str_key, c_str_value);
        }

        if (i < size - 1) {
            total_size += snprintf(NULL, 0, ", ");
        }

        Py_DECREF(str_key);
        Py_DECREF(str_value);
    }

    total_size += snprintf(NULL, 0, "}");
    buf = (char*) malloc(total_size + 1);

    int offset = 0;
    offset += snprintf(buf + offset, total_size - offset + 1, "{");
    for (int i = 0; i < size; i++) {
        PyObject* key = PyList_GetItem(keys, i);
        PyObject* value = PyList_GetItem(values, i);

        PyObject* str_key = PyObject_Str(key);
        PyObject* str_value = PyObject_Str(value);
        const char* c_str_key = PyUnicode_AsUTF8(str_key);
        const char* c_str_value = PyUnicode_AsUTF8(str_value);

        int n;

        if (PyNumber_Check(value)) {
            n = snprintf(buf + offset, total_size - offset + 1, "\"%s\": %s", c_str_key, c_str_value);
        } else {
            n = snprintf(buf + offset, total_size - offset + 1, "\"%s\": \"%s\"", c_str_key, c_str_value);
        }

        if (i < size - 1) {
            n += snprintf(buf + offset + n, total_size - offset - n + 1, ", ");
        }

        offset += n;

        Py_DECREF(str_key);
        Py_DECREF(str_value);
    }

    snprintf(buf + offset, total_size - offset + 1, "}");

    Py_DECREF(keys);
    Py_DECREF(values);

    PyObject* str = PyUnicode_FromString(buf);

    free(buf);

    return str;
}

static PyMethodDef methods[] = {
    {"loads", loads, METH_VARARGS, "Loads json."},
    {"dumps", dumps, METH_VARARGS, "Dumps json."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cutilsmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "Module for my first c api code.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create(&cutilsmodule);
}
