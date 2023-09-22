
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading;
using System.Xml.Linq;
using GameManagerService.Data;
using GameManagerService.Models;
using GameManagerService.Services;
using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;

namespace GameManager.Controllers;
[ApiController]
[Route("api/game")]
public class GameController : ControllerBase
{
    private readonly ILogger<GameController> _logger;

    private readonly ApDbContext _dbContext;
    private readonly IDatabase _redisDb;
    public GameController(
        ILogger<GameController> logger,
        IConnectionMultiplexer redis,
        ApDbContext dbContext)
    {
        _logger = logger;
        _redisDb = redis.GetDatabase();
        _dbContext = dbContext;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetGame(string id)
    {
        var expTime = DateTimeOffset.Now.AddMinutes(1);
        string data = _redisDb.StringGet($"{id}");
        if (data == null)
        {
            return NotFound();
        }

        return Ok(data);
    }

    [HttpPost("{id}")]
    public async Task<IActionResult> AddGame([FromRoute] string id)
    {
        byte[] requestData;
        using (var memoryStream = new MemoryStream())
        {
            Request.Body.CopyTo(memoryStream);
            requestData = memoryStream.ToArray();
            _redisDb.KeyDelete($"{id}");
            _redisDb.StringSet($"{id}", requestData);
            return Ok(requestData);
        }
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateGame(string id)
    {
        using var reader = new StreamReader(Request.Body);
        var body = await reader.ReadToEndAsync();
        _redisDb.KeyDelete($"{id}");
        _redisDb.StringSet($"{id}", body);
        return Ok(body);
    }


    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteGame(string id)
    {
        using var reader = new StreamReader(Request.Body);
        var body = await reader.ReadToEndAsync();
        _redisDb.KeyDelete($"{id}");
        return NoContent();
    }
}
