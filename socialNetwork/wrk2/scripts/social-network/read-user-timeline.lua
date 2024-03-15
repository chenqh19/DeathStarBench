local socket = require("socket")
local time = socket.gettime()*1000
math.randomseed(time)
math.random(); math.random(); math.random()

-- load env vars
local max_user_index = tonumber(os.getenv("max_user_index")) or 962

request = function()
  local user_id = tostring(math.random(0, max_user_index - 1))
  local start = math.random(0, 30)
  local stop = start + math.random(0, 20)
  start = tostring(start)
  stop = tostring(stop)
  local args = "user_id=" .. user_id .. "&start=" .. start .. "&stop=" .. stop
  local method = "GET"
  local headers = {}
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  local path = "http://ath-4:8080/wrk2-api/user-timeline/read?" .. args
  return wrk.format(method, path, headers, nil)

end
