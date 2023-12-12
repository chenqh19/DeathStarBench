package main

import (
	"os"
	"runtime/debug"
	// "strconv"
	// "strings"
	// "time"

	// "github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	// "github.com/bradfitz/gomemcache/memcache"
)

func changeGCPercent(percent int)	{
	prev := debug.SetGCPercent(percent)
	os.Setenv("GOGC", "50")
	log.Info().Msgf("Tune: setGCPercent to %d from %d", percent, prev)
}

func main() {
	changeGCPercent(50)
}

