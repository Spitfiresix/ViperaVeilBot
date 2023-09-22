using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;
using Newtonsoft.Json;
using GameManager.Dtos;

namespace GameManager.Controllers
{
    [Route("api/matchmaking")]
    [ApiController]
    public class MatchmakingController : ControllerBase
    {
        private readonly IDatabase _redisDb;
        private readonly MatchmakingQueue _matchmakingQueue;
        private const string MatchmakingKey = "matchmaking";
        private const string MatchKey = "match";
    
        public MatchmakingController(IConnectionMultiplexer redis, MatchmakingQueue matchmakingQueue)
        {
            _redisDb = redis.GetDatabase();
            _matchmakingQueue = matchmakingQueue;
        }

        [HttpPost("enqueue")]
        public IActionResult EnqueuePlayer(PlayerDto player)
        {
            // Convert the PlayerDTO to Player object
            var playerObj = new Player
            {
                Name = player.Name,
                SelectedModes = player.SelectedModes.ToList()
            };

            // Enqueue the player in the matchmaking queue
            _matchmakingQueue.Enqueue(playerObj, playerObj.SelectedModes);

            // Store the updated matchmaking queue back in Redis
            //SaveMatchmakingQueue(matchmakingQueue);

            return Ok();
        }

        [HttpPost("dequeue")]
        public IActionResult DequeuePlayer()
        {
            // Fetch the existing matchmaking queue from Redis or create a new one if it doesn't exist

            // Dequeue a player from the matchmaking queue
            _matchmakingQueue.Dequeue();

            // Store the updated matchmaking queue back in Redis
            //SaveMatchmakingQueue(matchmakingQueue);

            return Ok();
        }

        private void SaveMatchmakingQueue(MatchmakingQueue matchmakingQueue)
        {
            // Serialize the matchmaking queue to store it in Redis
            var serializedQueue = SerializeMatchmakingQueue(matchmakingQueue);
            _redisDb.StringSet(MatchmakingKey, serializedQueue);
        }

        private MatchmakingQueue DeserializeMatchmakingQueue(string serializedQueue)
        {
             return JsonConvert.DeserializeObject<MatchmakingQueue>(serializedQueue);
        }

        private string SerializeMatchmakingQueue(MatchmakingQueue matchmakingQueue)
        {
             return JsonConvert.SerializeObject(matchmakingQueue);

        }

        
    [HttpGet("has-match")]
    public IActionResult HasMatch()
    {
        var hasMatch = _redisDb.KeyExists(MatchKey);
        return Ok(hasMatch);
    }

    [HttpGet("get-match")]
    public IActionResult GetMatch()
    {
        var match = _redisDb.StringGet(MatchKey);
        if (match != String.Empty)
        {
            // Deserialize the match from Redis
            Match matchData = JsonConvert.DeserializeObject<Match>(match);
            return Ok(matchData);
        }

        return NotFound();
    }
    }
}
