local nk = require("nakama")

nk.run_once(function(context)
  nk.leaderboard_create("all_time_points", false, "desc", "incr")
end)