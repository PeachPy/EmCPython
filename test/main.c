#include <Python.h>

#include <stdio.h>
#include <fcntl.h>

#include <emscripten.h>

#include <libtar.h>

int main(int argc, char** argv) {
	printf("OPEN TAR FILE\n");
	TAR* tar;
	if (tar_open(&tar, "/pydata.tar", NULL, O_RDONLY, 0, 0) != 0) {
		fprintf(stderr, "Error: failed to open pydata.tar\n");
		exit(1);
	}

	printf("EXTRACT TAR FILE\n");
	if (tar_extract_all(tar, (char*) "/") != 0) {
		fprintf(stderr, "Error: failed to extract pydata.tar\n");
		exit(1);
	}
	printf("TAR EXTRACTION FINISHED\n");

	tar_close(tar);

	setenv("PYTHONHOME", "/", 0);

	printf("INITIALIZING CPYTHON\n");
	Py_InitializeEx(0);
	printf("CPYTHON INITIALIZATION FINISHED\n");

	PyRun_SimpleString("print \"Hello from Python\"");

	printf("FINALIZING CPYTHON\n");
	Py_Finalize();
	printf("CPYTHON FINALIZATION FINISHED\n");

	emscripten_exit_with_live_runtime();
	return 0;
}