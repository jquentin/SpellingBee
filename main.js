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

window.error = "";

window.submit_word = async function(word, language)
{
    console.log("SubmitWord: %s ; in language: %s", word, language);
    var session = await client.authenticateDevice(deviceId);
    var response = await client.rpc(session, "SubmitWord", JSON.stringify({ word: word, language: language }));
    console.log("SubmitWord response: %s", response);
}

window.get_todays_bee = async function (language, callback)
{
    var session = await client.authenticateDevice(deviceId);
    var response = await client.rpc(session, "GetTodaysBee", JSON.stringify({ language: language }));
    callback(response.payload);
}

window.get_yesterdays_bee = async function (language, callback)
{
    var session = await client.authenticateDevice(deviceId);
    var response = await client.rpc(session, "GetYesterdaysBee", JSON.stringify({ language: language }));
    callback(response.payload);
}

window.rpc = async function (id, input, callback)
{
    const session = await client.authenticateDevice(deviceId);
    const response = await client.rpc(session, id, input);
    callback(response.payload);
}

window.list_scores = async function (leaderboardId, callback)
{
    var session = await client.authenticateDevice(deviceId);
    var result = await client.rpc(session, "ListLeaderboard", JSON.stringify({ leaderboardId: leaderboardId }));
    scores = [];
    console.log(result.payload.records);
    result.payload.records.forEach(function(record) {
        console.log(record.username, record.score);
        scores.push({username: record.username, score: record.score});
    });
    callback(scores);
}

window.update_user = async function (callback)
{
    var session = await client.authenticateDevice(deviceId);
    var account = await client.getAccount(session);
    callback(account.user.username);
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
