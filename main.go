package main

import (
	"encoding/json"
	"melty/internal/memory"
	"melty/internal/process"
	"net/http"
)

var p_id int = -1

func meltyStatus(w http.ResponseWriter, r *http.Request) {
	data := map[string]any{
		"waiting": true,
	}

	if _, err := memory.IsMeltyAlive(); err != nil {
		if n_id, err := process.GetProcessIDWithName("MBAA"); err == nil {
			if _, err := memory.SetupMelty(n_id); err == nil {
				p_id = n_id
			}
		}
	}

	if p_id != -1 {
		new_data := memory.ReadMelty(p_id)

		for key, value := range new_data {
			data[key] = value
		}

		data["waiting"] = false
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(data)
}

func main() {
	http.Handle("/", http.FileServer(http.Dir("./web/dist")))
	http.HandleFunc("/state", meltyStatus)
	http.ListenAndServe(":8080", nil)
}
