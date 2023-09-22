using System.Diagnostics;
using Newtonsoft.Json;
using StackExchange.Redis;

namespace GameManagerService.Services{
public class MatchmakingProcess : IMatchmakingProcess
{
    private readonly MatchmakingQueue _matchmakingQueue;
    private readonly Timer _timer;
    private readonly IConnectionMultiplexer _redis;
    public MatchmakingProcess(IConnectionMultiplexer redis)
    {
        _redis = redis;
        _matchmakingQueue = new MatchmakingQueue();
        _timer = new Timer(CheckMatchmakingQueue, null, TimeSpan.Zero, TimeSpan.FromSeconds(10));
    }

private void CheckMatchmakingQueue(object state)
{
    if (_matchmakingQueue.HasMatch(out int matchedMode, out List<Player> matchedPlayers))
    {
        // Match found, create a new Match instance and pass the players
        // Perform team captain selection and team assignment based on your configuration

        // Create a new Match instance with the players and teams
        Match match = new Match(matchedPlayers, matchedMode, "random_team" );
        _redis.GetDatabase().StringSet("match", JsonConvert.SerializeObject(match));
        // Store the Match in the cache, 
        //Let the discord bot pick up the match from the cache through match controller, 
        //and send the match details to the players
        // ...
    }
    else
    {
        _matchmakingQueue.Dequeue();
    }
    Debug.WriteLine("Matchmaking queue checked");
}

    public void Stop()
    {
        _timer.Dispose();
    }
}
}