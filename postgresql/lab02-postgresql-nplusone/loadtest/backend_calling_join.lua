-- Gera customer_id aleatório e chama o endpoint correto (JOIN)
-- /customers/{id}/products/join

math.randomseed(os.time())

-- Ajuste o range conforme definido no ds_generator
local MIN_ID = 1
local MAX_ID = 10000

request = function()
  local customer_id = math.random(MIN_ID, MAX_ID)
  local path = "/customers/" .. customer_id .. "/products/join"

  return wrk.format("GET", path)
end
