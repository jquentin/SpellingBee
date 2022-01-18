const nakamajs = require ("@heroiclabs/nakama-js");
const uuid = require("uuid")

var client = new nakamajs.Client("defaultkey", "164.92.227.165", 7350);

try {
    var deviceId = localStorage.getItem("deviceId");
    if (!deviceId)
    {
        console.log("can't find");
        deviceId = uuid.v4();
        localStorage.setItem("deviceId", deviceId);
    }
    console.log(deviceId);
}
catch (err) {
    console.log("Error authenticating device: %o:%o", err.statusCode, err.message);
}

var socket = client.createSocket();

window.all_scores = {};

window.username = "";

window.increment_score = async function(leaderboardId, amount)
{
    var session = await client.authenticateDevice(deviceId);

    var submission = {score: amount};
    var record = await client.writeLeaderboardRecord(session, leaderboardId, submission);
    console.log("New record username %o and score %o", record.username, record.score);
}

window.list_scores = async function (leaderboardId)
{
    window.all_scores[leaderboardId] = {};
    var session = await client.authenticateDevice(deviceId);
    var result = await client.listLeaderboardRecords(session, leaderboardId);
    result.records.forEach(function(record) {
        window.all_scores[leaderboardId][record.username] = record.score;
    });
    while (result.next_cursor) {
      result = await client.listLeaderboardRecords(session, leaderboardId, null, null, result.next_cursor);
      result.records.forEach(function(record) {
          window.all_scores[leaderboardId][record.username] = record.score;
      });
    }
    
}

window.update_user = async function ()
{
    var session = await client.authenticateDevice(deviceId);
    var account = await client.getAccount(session);
    window.username = account.user.username;
}

window.change_username = async function (username)
{
    try
    {
        console.log("change_username", username);
        var session = await client.authenticateDevice(deviceId);
        await client.updateAccount(session, {
            username: username,
            display_name: username
        });
    }
    catch (e)
    {
        console.log(e);
    }
}
