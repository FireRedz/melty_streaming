// Taken from https://gist.github.com/RednibCoding/4d9e1a3dc309cfd5f5af3089a67abac0
package memory

import (
	"fmt"
	"syscall"
	"unsafe"
)

type Process uintptr

var kernel32 = syscall.MustLoadDLL("kernel32.dll")

const PROCESS_VM_READ = 0x0010
const PROCESS_ALL_ACCESS = 0x1F0FFF

var procOpenProcess = kernel32.MustFindProc("OpenProcess")
var procReadProcessMemory = kernel32.MustFindProc("ReadProcessMemory")

// Wrapper function for OpenProcess
func OpenProcessHandle(processId int, access int) Process {
	handle, _, _ := procOpenProcess.Call(ptr(access), ptr(false), ptr(processId))

	return Process(handle)
}

// Wrapper function for ReadProcessMemory
func ReadProcessMemory(handle Process, address uintptr, buffer []byte, nSize uintptr, length uint32) (int32, error) {
	ret, _, e := procReadProcessMemory.Call(
		uintptr(handle),
		address,
		uintptr(unsafe.Pointer(&buffer[0])),
		nSize,
		uintptr(unsafe.Pointer(&length)))

	if ret == 0 {
		return 0, fmt.Errorf("ReadProcessMemory failed with error: %v", e)
	}

	return bytesToInt(buffer), nil
}

// Converts >= 4 byte array to int32
func bytesToInt(byteArray []byte) int32 {
	if len(byteArray) < 4 {
		return 0
	}

	return int32(byteArray[0]) | int32(byteArray[1])<<8 | int32(byteArray[2])<<16 | int32(byteArray[3])<<24
}

// Converts types
func ptr(val interface{}) uintptr {
	switch v := val.(type) {
	case string:
		ptr, err := syscall.UTF16PtrFromString(v)
		if err != nil {
			return uintptr(0)
		}
		return uintptr(unsafe.Pointer(ptr))
	case int:
		return uintptr(v)
	default:
		return uintptr(0)
	}
}
