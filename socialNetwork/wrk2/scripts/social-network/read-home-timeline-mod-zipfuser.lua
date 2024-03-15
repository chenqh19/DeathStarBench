local socket = require("socket")
local time = socket.gettime()*1000
math.randomseed(time)
math.random(); math.random(); math.random()

-- Function to sample a number within a given range using Zipfian distribution
-- function sampleZipfianInRange(min_value, max_value, alpha)
--   local values = {}
--   local c = 0 -- Normalization constant

--   -- Calculate normalization constant
--   for i = min_value, max_value do
--       c = c + (1 / math.pow(i, alpha))
--   end

--   -- Generate values with probabilities
--   for i = min_value, max_value do
--       local probability = 1 / (math.pow(i, alpha) * c)
--       table.insert(values, {i, probability})
--   end

--   -- Sample a value based on probabilities
--   local random_value = math.random()
--   local cumulative_probability = 0
--   for _, pair in ipairs(values) do
--       cumulative_probability = cumulative_probability + pair[2]
--       if random_value <= cumulative_probability then
--           return pair[1]
--       end
--   end
-- end

-- Example usage
-- local min_value = 1
-- local max_value = 10
-- local alpha = 1

-- Sample a value
-- local sampled_value = sampleZipfianInRange(min_value, max_value, alpha)
-- print("Sampled value:", sampled_value)

-- load env vars
local max_user_index = tonumber(os.getenv("max_user_index")) or 961
local alpha = 1
local values = {}
local c = 0 -- Normalization constant

-- Calculate normalization constant
for i = 0, max_user_index - 1 do
    c = c + (1 / math.pow(i, alpha))
end

-- Generate values with probabilities
for i = 0, max_user_index - 1 do
    local probability = 1 / (math.pow(i, alpha) * c)
    table.insert(values, {i, probability})
end


request = function()
  -- local user_id = tostring(math.random(0, max_user_index - 1))
  local user_id = 0

  -- Sample a value based on probabilities
  local random_value = math.random()
  local cumulative_probability = 0
  for _, pair in ipairs(values) do
      cumulative_probability = cumulative_probability + pair[2]
      if random_value <= cumulative_probability then
          user_id = pair[1]
          break
      end
  end


  local start = tostring(math.random(0, 10))
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
