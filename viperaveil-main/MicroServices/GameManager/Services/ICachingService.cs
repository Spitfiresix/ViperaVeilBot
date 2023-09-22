namespace GameManagerService.Services
{
    public interface ICachingService
    {
        T GetData<T>(string key);
        bool SetData<T>(string key, T value, DateTimeOffset expTime);
        object  RemoveData(string key);
    }
}