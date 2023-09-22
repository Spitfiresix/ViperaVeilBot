using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;

namespace GameManager.Controllers
{
    [Route("api/leaderboard")]
    [ApiController]
    public class LeaderboardController : ControllerBase
    {
        private readonly IDatabase _redisDb;

        public LeaderboardController(IConnectionMultiplexer redis)
        {
            _redisDb = redis.GetDatabase();
        }

        [HttpPost("add")]
        public IActionResult AddPlayerToLeaderboard(LeaderBoardEntryDto player)
        {
            _redisDb.SortedSetAdd($"leaderboard:{player.GameMode}", player.PlayerName, player.Score);
            return Ok();
        }

        [HttpGet("{gameMode}")]
        public IActionResult GetLeaderboard(string gameMode)
        {
            var leaderboard = _redisDb.SortedSetRangeByRankWithScores($"leaderboard:{gameMode}", 0, -1, Order.Descending);
            var result = leaderboard.Select(entry => new LeaderBoardEntryDto
            {
                PlayerName = entry.Element,
                Score = (int)entry.Score,
                GameMode = gameMode
            }).ToList();

            return Ok(result);
        }
    }
}
