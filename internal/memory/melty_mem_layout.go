package memory

import "fmt"

const MELTY_HEADER = 4194304

type MemoryLocation struct {
	key      string
	location int
	size     int
}

var states = []MemoryLocation{
	{"gamemode", 5566184, 1},
	{"p1selmode", 7657708, 1},
	{"p1char", 7657724, 1},
	{"p1moon", 7657728, 1},
	{"p1heat", 5591576, 1},
	{"p2selmode", 7657744, 1},
	{"p2char", 7657760, 1},
	{"p2moon", 7657764, 1},
	{"p2heat", 5594388, 1},
}

var melty_handle Process
var melty_buf = make([]byte, 8)
var melty_last_length = uint32(0)

func SetupMelty(p_id int) (bool, error) {
	melty_handle = OpenProcessHandle(p_id, PROCESS_ALL_ACCESS)

	if melty_handle != 0 {
		return true, nil
	}

	return false, fmt.Errorf("failed to set up the melty memory reader")
}

func ReadMelty(p_id int) map[string]int {
	live := make(map[string]int) // Create map locally for each read cycle

	for _, mem_to_read := range states {
		value, err := ReadProcessMemory(melty_handle, uintptr(mem_to_read.location), melty_buf, uintptr(mem_to_read.size), melty_last_length)

		if err == nil {
			live[mem_to_read.key] = int(value)
		}

	}

	return live
}

func IsMeltyAlive() (int, error) {
	buf := make([]byte, 4)

	value, err := ReadProcessMemory(melty_handle, uintptr(MELTY_HEADER), buf, uintptr(1), melty_last_length)

	if err == nil {
		return int(value), nil
	}

	return 0, fmt.Errorf("process not alive")
}
