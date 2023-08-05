#include "igeCamera.h"
#include "igeCamera_doc_en.h"

PyObject* camera_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	camera_obj* self = NULL;

	self = (camera_obj*)type->tp_alloc(type, 0);
	self->camera = Camera::Instance();

	return (PyObject*)self;
}

void camera_dealloc(camera_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* camera_str(camera_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "ige camera object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* camera_Init(camera_obj* self)
{
	Camera::Instance()->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* camera_Release(camera_obj* self)
{
	Camera::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* camera_GetCameraSize(camera_obj* self)
{
	PyObject* cameraSize = Py_BuildValue("{s:i,s:i}",
		"w", Camera::Instance()->getCameraWidth(),
		"h", Camera::Instance()->getCameraHeight());
	

	return cameraSize;
}

static PyObject* camera_GetCameraData(camera_obj* self)
{
	uint8_t* result = Camera::Instance()->getCameraData();
	PyObject* obj = PyBytes_FromStringAndSize((char*)result, Camera::Instance()->getCameraWidth() * Camera::Instance()->getCameraHeight() * 3);

	return obj;
}


PyMethodDef camera_methods[] = {
	{ "init", (PyCFunction)camera_Init, METH_NOARGS, cameraInit_doc },
	{ "release", (PyCFunction)camera_Release, METH_NOARGS, cameraRelease_doc },
	{ "getCameraSize", (PyCFunction)camera_GetCameraSize, METH_NOARGS, cameraGetCameraSize_doc },
	{ "getCameraData", (PyCFunction)camera_GetCameraData, METH_NOARGS, cameraGetCameraData_doc },
	{ NULL,	NULL }
};

PyGetSetDef camera_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject CameraType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeCamera.camera",							/* tp_name */
	sizeof(camera_obj),							/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)camera_dealloc,					/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)camera_str,						/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	camera_methods,								/* tp_methods */
	0,											/* tp_members */
	camera_getsets,								/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	camera_new,									/* tp_new */
	0,											/* tp_free */
};


static PyModuleDef camera_module = {
	PyModuleDef_HEAD_INIT,
	"igeCamera",						// Module name to use with Python import statements
	"Camera Module.",					// Module description
	0,
	camera_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeCamera() {
	PyObject* module = PyModule_Create(&camera_module);

	if (PyType_Ready(&CameraType) < 0) return NULL;

	return module;
}
