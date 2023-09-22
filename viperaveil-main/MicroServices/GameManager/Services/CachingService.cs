using System.Text.Json;
using GameManagerService.Services;
using StackExchange.Redis;

public class CachingService : ICachingService
{
    private readonly IDatabase _cacheDb;

    public CachingService(IConnectionMultiplexer cache)
    {
        _cacheDb = cache.GetDatabase();
    }
    public T GetData<T>(string key)
    {
        var value = _cacheDb.StringGet(key);
        if (value.HasValue)
        {
            return JsonSerializer.Deserialize<T>(value);
        }
        return default;
    }
    public bool SetData<T>(string key, T value, DateTimeOffset expTime)
    {
        var expTimeSpan = expTime.Subtract(DateTimeOffset.Now);
        return _cacheDb.StringSet(key, JsonSerializer.Serialize(value), expTimeSpan);
        
    }

    public object RemoveData(string key)
    {
        var value = _cacheDb.KeyExists(key);
        if (value)
        {
            return _cacheDb.KeyDelete(key);
        }

        return false;
    }
}