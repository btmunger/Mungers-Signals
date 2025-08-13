#include <stdio.h>
#include <Python.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // Initialize the Python interpreter
    Py_Initialize();

    // Relative path to main script
    const char *script_path = "./bootstrap.py";

    // Open the Python script file
    FILE *fp = fopen(script_path, "r");
    if (fp != NULL) {
        PyRun_SimpleFile(fp, script_path);
        fclose(fp);
    } else {
        printf("Could not open Python script: %s\n", script_path);
    }

    // Finalize the Python interpreter
    Py_Finalize();

    return 0;
}

/* Rebuild .exe application (signature will have to be reset)*/
// gcc wrapper.c gui/icon/icon.res -IC:/Python313/include -LC:/Python313/libs -lpython313 -o MungersSignals.exe -mwindows
/* Uninstall all pip packages */
// pip freeze | % { $_.split('==')[0] } | % { pip uninstall -y $_ }