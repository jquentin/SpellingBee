local nk = require("nakama")

nk.run_once(function(context)

  nk.leaderboard_create("all_time_points", false, "desc", "incr")
  
  nk.leaderboard_create("all_time_points_en", false, "desc", "incr")
  nk.leaderboard_create("all_time_points_fr", false, "desc", "incr")
  
  nk.leaderboard_create("daily_points_mon_en", false, "desc", "incr", "0 0 * * THU")
  nk.leaderboard_create("daily_points_tue_en", false, "desc", "incr", "0 0 * * FRI")
  nk.leaderboard_create("daily_points_wed_en", false, "desc", "incr", "0 0 * * SAT")
  nk.leaderboard_create("daily_points_thu_en", false, "desc", "incr", "0 0 * * SUN")
  nk.leaderboard_create("daily_points_fri_en", false, "desc", "incr", "0 0 * * MON")
  nk.leaderboard_create("daily_points_sat_en", false, "desc", "incr", "0 0 * * TUE")
  nk.leaderboard_create("daily_points_sun_en", false, "desc", "incr", "0 0 * * WED")
  
  nk.leaderboard_create("daily_points_mon_fr", false, "desc", "incr", "0 0 * * THU")
  nk.leaderboard_create("daily_points_tue_fr", false, "desc", "incr", "0 0 * * FRI")
  nk.leaderboard_create("daily_points_wed_fr", false, "desc", "incr", "0 0 * * SAT")
  nk.leaderboard_create("daily_points_thu_fr", false, "desc", "incr", "0 0 * * SUN")
  nk.leaderboard_create("daily_points_fri_fr", false, "desc", "incr", "0 0 * * MON")
  nk.leaderboard_create("daily_points_sat_fr", false, "desc", "incr", "0 0 * * TUE")
  nk.leaderboard_create("daily_points_sun_fr", false, "desc", "incr", "0 0 * * WED")
  
end)

