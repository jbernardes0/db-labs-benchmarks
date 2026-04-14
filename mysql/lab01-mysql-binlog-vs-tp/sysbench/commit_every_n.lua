sysbench.cmdline.options = {
  inserts_per_tx = {
    "Number of INSERTs per transaction",
    10
  }
}

function thread_init()
  drv = sysbench.sql.driver()
  con = drv:connect()

  math.randomseed(os.time() + sysbench.tid)
end

function thread_done()
  con:disconnect()
end

function event()
  local inserts_per_tx = sysbench.opt.inserts_per_tx

  con:query("BEGIN")

  for i = 1, inserts_per_tx do
    local k = math.random(1, 100000)
    local c = string.rep("x", 50)
    local pad = string.rep("y", 60)

    con:query(string.format(
      "INSERT INTO sbtest1 (k, c, pad) VALUES (%d, '%s', '%s')",
      k, c, pad
    ))
  end

  con:query("COMMIT")
end