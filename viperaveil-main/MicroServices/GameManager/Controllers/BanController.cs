using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;
using System;
using System.Collections.Generic;

namespace YourNamespace.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BanController : ControllerBase
    {
        private readonly IConnectionMultiplexer _redis;

        public BanController(IConnectionMultiplexer redis)
        {
            _redis = redis;
        }

        [HttpPost]
        public IActionResult AddBan([FromBody] BanDTO ban)
        {
            var banKey = $"ban:{ban.UserId}";

            var values = new HashEntry[]
            {
                new HashEntry("UserId", ban.UserId),
                new HashEntry("DateNow", ban.DateNow.ToString("O")),
                new HashEntry("TimeEnd", ban.TimeEnd.ToString("O")),
                new HashEntry("Reason", ban.Reason)
            };

            _redis.GetDatabase().HashSet(banKey, values);

            return Ok();
        }

        [HttpGet]
        public IActionResult GetBans()
        {
            //Fix later
            // string redisHost = Configuration["Redis:Host"]; // Replace "Redis:Host" with the actual key in your configuration file

            // var redis = ConnectionMultiplexer.Connect(redisHost);
            // var database = redis.GetDatabase();

            // long cursor = 0;
            // var banKeys = new List<RedisKey>();

            // do
            // {
            //     var scanResult = database.Execute("SCAN", cursor.ToString(), "MATCH", "ban:*");
            //     cursor = (long)scanResult[0];
            //     var keys = (RedisResult[])scanResult[1];

            //     foreach (var key in keys)
            //     {
            //         banKeys.Add((RedisKey)key);
            //     }
            // }
            // while (cursor != 0);

            // var bans = new List<BanDTO>();

            // foreach (var banKey in banKeys)
            // {
            //     var banValues = database.HashGetAll(banKey);

            //     var ban = new BanDTO
            //     {
            //         UserId = banValues["UserId"],
            //         DateNow = DateTime.ParseExact(banValues["DateNow"], "O", null),
            //         TimeEnd = DateTime.ParseExact(banValues["TimeEnd"], "O", null),
            //         Reason = banValues["Reason"]
            //     };

            //     bans.Add(ban);
            // }

            //return Ok(bans);
            return Ok();
        }


        [HttpPost("{userId}/unban")]
        public IActionResult Unban(int userId)
        {
            var banKey = $"ban:{userId}";

            _redis.GetDatabase().KeyDelete(banKey);

            return Ok();
        }
    }
}
