using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;

namespace GameManager.Controllers
{
    [Route("api/gamemodes")]
    [ApiController]
    public class GameModesController : ControllerBase
    {
        private readonly IDatabase _redisDb;

        public GameModesController(IConnectionMultiplexer redis)
        {
            _redisDb = redis.GetDatabase();
        }

        [HttpPost("add/{mode}")]
        public IActionResult AddGameMode([FromRoute]string mode)
        {
            _redisDb.SetAdd("gamemodes", mode);
            return Ok();
        }

        [HttpGet]
        public IActionResult GetGameModes()
        {   
            //Hard code game modes 
            // 1s, 2s, 3s, 4s,
            string[] modes = {"1s", "2s", "3s", "4s"};
            //var gameModes = _redisDb.SetMembers("gamemodes").ToStringArray();
            return Ok(modes);
        }

        [HttpDelete("{mode}")]
        public IActionResult DeleteGameModes(string mode)
        {
            _redisDb.KeyDelete(mode);
            return NoContent();
        }
    }
}
