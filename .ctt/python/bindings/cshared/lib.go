// Package main exposes test-template as a C shared library.
//
// Every exported function recovers from panics because a panic crossing the cgo
// boundary terminates the host process, which for a Python caller means killing
// the interpreter rather than raising. For the same reason nothing here may call
// os.Exit.
package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"strings"
	"unsafe"
)

var (
	version = "dev"
	commit  = "none"
	date    = "unknown"
)

// TestTemplateRun applies the library to input and returns a malloc'd C string
// the caller owns. On failure it returns NULL and writes a malloc'd message to
// errOut. Both pointers must be released with TestTemplateFree.
//
//export TestTemplateRun
func TestTemplateRun(input *C.char, errOut **C.char) (result *C.char) {
	defer func() {
		if r := recover(); r != nil {
			result = nil
			setError(errOut, panicMessage(r))
		}
	}()

	*errOut = nil

	return C.CString(strings.TrimSpace(C.GoString(input)))
}

// TestTemplateVersion returns a malloc'd "version commit date" triple for the caller to free.
//
//export TestTemplateVersion
func TestTemplateVersion() *C.char {
	return C.CString(version + " " + commit + " " + date)
}

// TestTemplateFree releases a pointer returned by any other exported function.
//
//export TestTemplateFree
func TestTemplateFree(p *C.char) {
	if p != nil {
		C.free(unsafe.Pointer(p))
	}
}

func setError(errOut **C.char, message string) {
	if errOut != nil {
		*errOut = C.CString(message)
	}
}

func panicMessage(r any) string {
	if err, ok := r.(error); ok {
		return err.Error()
	}

	if s, ok := r.(string); ok {
		return s
	}

	return "unknown panic in test-template"
}

func main() {}
