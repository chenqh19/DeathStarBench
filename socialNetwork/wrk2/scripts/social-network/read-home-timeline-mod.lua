local socket = require("socket")
local time = socket.gettime()*1000
math.randomseed(time)
math.random(); math.random(); math.random()

-- load env vars
local max_user_index = tonumber(os.getenv("max_user_index")) or 961

request = function()
  local user_id = tostring(math.random(0, max_user_index - 1))
  local start = tostring(math.random(0, 30))
  local stop = tostring(start + math.random(0, 20))

  local args = "user_id=" .. user_id .. "&start=" .. start .. "&stop=" .. stop
  -- local args = "user_id=132&start=0&stop=23"
  local method = "GET"
  local headers = {}
  -- headers["Content-Type"] = "application/x-www-form-urlencoded"
  -- headers["User-Agent"] = "wrk"
  -- headers["Accept"] = "wrk"
  -- headers["Content-Type"] = "application/json"
  -- body = '{"userid" : ' .. user_id .. ', "start" : ' .. start .. ', "stop" : ' .. stop  .. ' }'
  local path = "/home?" .. args 
  -- local body = "user_id=" .. wrk.format("0") .. "&start=" .. wrk.format("1") .. "&stop=" .. wrk.format("5")
  -- local body = "user_id=0&start=1&stop=3"
  local response =  wrk.format(method, path, headers, nil)
  -- print(response)
  return response
end
