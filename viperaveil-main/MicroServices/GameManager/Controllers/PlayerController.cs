using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;
using Newtonsoft.Json;

namespace GameManager.Controllers
{
    [Route("api/players")]
    [ApiController]
    public class PlayersController : ControllerBase
    {
        private readonly IDatabase _redisDb;
        private const string PlayersKey = "players";

        public PlayersController(IConnectionMultiplexer redis)
        {
            _redisDb = redis.GetDatabase();
        }

        [HttpPost("add")]
        public IActionResult AddPlayer(PlayerDto player)
        {
            var serializedPlayer = Newtonsoft.Json.JsonConvert.SerializeObject(player);

            // Add the serialized player to Redis set
            _redisDb.SetAdd(PlayersKey, serializedPlayer);

            return Ok();
        }

        [HttpGet]
        public IActionResult GetPlayers()
        {
            var serializedPlayers = _redisDb.SetMembers(PlayersKey);

            // Deserialize and return the list of players
            var players = new List<PlayerDto>();
            foreach (var serializedPlayer in serializedPlayers)
            {
                var player = Newtonsoft.Json.JsonConvert.DeserializeObject<PlayerDto>(serializedPlayer);
                players.Add(player);
            }

            return Ok(players);
        }

        [HttpGet("{id}")]
        public IActionResult GetPlayer([FromRoute] string id)
        {
            var serializedPlayers = _redisDb.SetMembers(PlayersKey);

            foreach (var serializedPlayer in serializedPlayers)
            {
                var player = Newtonsoft.Json.JsonConvert.DeserializeObject<PlayerDto>(serializedPlayer);

                if (player?.UserId.ToString() == id)
                {
                    return Ok(player);
                }
            }

            return NotFound();
        }


        [HttpDelete("{playerName}")]
        public IActionResult RemovePlayer(string playerName)
        {
            var serializedPlayer = _redisDb.SetMembers(PlayersKey);
            var player = serializedPlayer;
                player.FirstOrDefault(p => p == (playerName));

            if (serializedPlayer != null)
            {
                _redisDb.SetRemove(PlayersKey, serializedPlayer);
                return Ok();
            }
            else
            {
                return NotFound();
            }
        }
    }
}
