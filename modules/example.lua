local nk = require("nakama")

nk.run_once(function(context)
  nk.leaderboard_create("all_time_points", false, "desc", "incr")
  nk.leaderboard_create("all_time_points_en", false, "desc", "incr")
  nk.leaderboard_create("all_time_points_fr", false, "desc", "incr")
  nk.leaderboard_create("daily_points_en", false, "desc", "incr")
  nk.leaderboard_create("daily_points_fr", false, "desc", "incr")
end)