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
console.log("deviceId", deviceId);

var socket = client.createSocket();

window.username = "";

window.error = "";

window.increment_score = async function(leaderboardId, amount)
{
    var session = await client.authenticateDevice(deviceId);

    var submission = {score: amount};
    var record = await client.writeLeaderboardRecord(session, leaderboardId, submission);
    console.log("New record username %o and score %o", record.username, record.score);
}

window.list_scores = async function (leaderboardId, callback)
{
    scores = {};
    var session = await client.authenticateDevice(deviceId);
    var result = await client.listLeaderboardRecords(session, leaderboardId);
    result.records.forEach(function(record) {
        scores[record.username] = record.score;
    });
    while (result.next_cursor) {
      result = await client.listLeaderboardRecords(session, leaderboardId, null, null, result.next_cursor);
      result.records.forEach(function(record) {
          scores[record.username] = record.score;
      });
    }
    callback(scores);
}

window.update_user = async function ()
{
    var session = await client.authenticateDevice(deviceId);
    var account = await client.getAccount(session);
    window.username = account.user.username;
    console.log(session)
    
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

window.connect_email = async function (email, password)
{
    window.error = "";
    const DEVICE_KEY = "device";
    console.log("Attempting to connect to email: ", email, " with password ", password);
    var emailAccountExists = false;
    try
    {
        const create = false;
        console.log("authenticateEmail");
        const remoteSession = await client.authenticateEmail(email, password, create, "username");
        emailAccountExists = true;
        console.log("emailAccountExists");
        var localSession = await client.authenticateDevice(deviceId);
        var ghostedAccountDeviceId = uuid.v4();
        console.log("linkDevice to ghost", ghostedAccountDeviceId);
        await client.linkDevice(localSession, {id: ghostedAccountDeviceId});
        console.log("unlinkDevice from ghost", deviceId);
        await client.unlinkDevice(localSession, {id: deviceId});
        console.log("linkDevice to remote session", deviceId);
        await client.linkDevice(remoteSession, {id: deviceId});
        console.log("linked Device");
        localStorage.setItem("email", email);
    }
    catch(e)
    {
        e.text().then(errMsg => { window.error += JSON.parse(errMsg).message + "\n"; console.log(window.error) });
        if (emailAccountExists)
            return;
        var session = await client.authenticateDevice(deviceId);
        try
        {
            await client.linkEmail(session, {email: email, password: password});
            console.info("Successfully linked");
            localStorage.setItem("email", email);
        }
        catch(e)
        {
            e.text().then(errMsg => { window.error += JSON.parse(errMsg).message + "\n"; console.log(window.error)});
        }
    }
}
