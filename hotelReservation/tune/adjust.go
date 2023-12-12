package tune

import (
	"os"
	"runtime/debug"
	"strconv"
	"strings"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/bradfitz/gomemcache/memcache"
)

func main() {
	tune.changeGCPercent(100)
}