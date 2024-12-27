package process

import (
	"fmt"
	"os/exec"
	"runtime"
	"strconv"
	"strings"
)

func GetProcessIDWithName(exe_name string) (int, error) {
	cur_cmd := exec.Command("tasklist")

	output, err := cur_cmd.CombinedOutput()

	if err != nil {
		return 0, fmt.Errorf("failed to get process id with the name '%s' because %v", exe_name, err)
	}

	output_str := string(output)

	for _, line := range strings.Split(output_str, "\n") {
		if runtime.GOOS == "windows" {
			if strings.HasPrefix(line, exe_name) {
				// bit scuffed but whatever
				parts := strings.Fields(line)

				if len(parts) > 1 {
					p_id, err := strconv.Atoi(parts[1])

					if err == nil {
						return p_id, nil
					}
				}
			}
		} else if runtime.GOOS == "linux" {
			parts := strings.Split(line, ",")

			if len(parts) > 1 {
				p_id, err := strconv.Atoi(parts[1])

				if err == nil {
					return p_id, nil
				}
			}
		}
	}

	return 0, fmt.Errorf("process '%s' not found", exe_name)
}
