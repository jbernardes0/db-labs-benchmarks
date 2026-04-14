
require("sysbench")

local inserts_per_tx = 10

function thread_init()
  drv = sysbench.sql.driver()
  con = drv:connect()
end

function thread_done()
  con:disconnect()
end

function event()
  con:query("BEGIN")

  for i = 1, inserts_per_tx do
    con:query(string.format(
      "INSERT INTO sbtest1 (k, c, pad) VALUES (%d, 'test', 'test')",
      math.random(1, 100000)
    ))
  end

  con:query("COMMIT")
end
EOF
