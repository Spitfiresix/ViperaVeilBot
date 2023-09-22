using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System;
using System.Net.Http;
using System.Text;
using Newtonsoft.Json;
using snekwarselo.Utilities;

namespace snekwarselo.Managers
{

        public class GameManagerClient
        {
            private string _BaseUrl { get; set; }
            private readonly HttpClient _httpClient;

            public GameManagerClient(string baseUrl)
            {
                _httpClient = new HttpClient();
                _BaseUrl = baseUrl;
            }

            public async Task<bool> AddPlayer(PlayerDto player)
            {
                var serializedPlayer = JsonConvert.SerializeObject(player);

                var url = $"{_BaseUrl}/api/players/add";
                var content = new StringContent(serializedPlayer, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Player added successfully.");
                    return true;
                }
                else
                {
                    Console.WriteLine("Failed to add player. Error: " + response.ReasonPhrase);
                    return false;
                }
            }

            public async Task<List<PlayerDto>> GetPlayers()
            {
                var url = $"{_BaseUrl}/api/players";
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    var players = JsonConvert.DeserializeObject<List<PlayerDto>>(content);
                    return players;
                }

                throw new Exception("Failed to get players. Error: " + response.ReasonPhrase);
            }


            public async Task<PlayerDto> GetPlayer(string playerId)
            {
                var url = $"{_BaseUrl}/api/players/{playerId}";
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    var player = JsonConvert.DeserializeObject<PlayerDto>(content);
                    return player;
                }

                if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return null; // Player not found
                }

                throw new Exception("Failed to get player. Error: " + response.ReasonPhrase);
            }

            public async Task<bool> RemovePlayer(string playerName)
            {
                var url = $"{_BaseUrl}/api/players/{playerName}";
                var response = await _httpClient.DeleteAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    return true; // Player removed successfully
                }

                if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return false; // Player not found
                }

                throw new Exception("Failed to remove player. Error: " + response.ReasonPhrase);
            }

            public async Task<QueueResponses> EnqueuePlayer(PlayerDto player)
            {
                var serializedPlayer = JsonConvert.SerializeObject(player);

                var url = $"{_BaseUrl}/api/matchmaking/enqueue";
                var content = new StringContent(serializedPlayer, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                return QueueResponses.Success;
                }
                else
                {
                return QueueResponses.Failed;
                }
            return QueueResponses.None;
            }

            public async Task<QueueResponses> DequeuePlayer()
            {
                var url = $"{_BaseUrl}/api/matchmaking/dequeue";

                var response = await _httpClient.PostAsync(url, null);

                if (response.IsSuccessStatusCode)
                {
                return QueueResponses.Success;
                }
                else
                {
                return QueueResponses.Failed;
            }
            }

            public async Task AddBan(BanDTO ban)
            {
                var serializedBan = JsonConvert.SerializeObject(ban);

                var url = $"{_BaseUrl}/api/matchmaking";
                var content = new StringContent(serializedBan, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Ban added successfully.");
                }
                else
                {
                    Console.WriteLine("Failed to add ban. Error: " + response.ReasonPhrase);
                }
            }

            public async Task<bool> CallUnbanApi(int userId)
            {
                var apiUrl = $"{_BaseUrl}/{userId}/unban";

                try
                {
                    var response = await _httpClient.PostAsync(apiUrl, null);

                    if (response.IsSuccessStatusCode)
                    {
                        return true;
                    }
                    else
                    {
                        // Handle the unsuccessful response
                        // e.g., log error or throw an exception
                        return false;
                    }
                }
                catch (Exception ex)
                {
                    // Handle the exception
                    // e.g., log error or throw an exception
                    return false;
                }
            }

            public async Task<bool> AddPlayerToLeaderboard(string playerName, int score, string gameMode)
            {
                var apiUrl = $"{_BaseUrl}/add";

                try
                {
                    var player = new LeaderBoardEntryDto
                    {
                        PlayerName = playerName,
                        Score = score,
                        GameMode = gameMode
                    };
                var serializedPlayer = Newtonsoft.Json.JsonConvert.SerializeObject(player);
                var content = new StringContent(serializedPlayer, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(apiUrl, content);

                    if (response.IsSuccessStatusCode)
                    {
                        return true;
                    }
                    else
                    {
                        // Handle the unsuccessful response
                        // e.g., log error or throw an exception
                        return false;
                    }
                }
                catch (Exception ex)
                {
                    // Handle the exception
                    // e.g., log error or throw an exception
                    return false;
                }
            }

            public async Task<List<LeaderBoardEntryDto>> GetLeaderboard(string gameMode)
            {
                var apiUrl = $"{_BaseUrl}/{gameMode}";

                try
                {
                    var response = await _httpClient.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {

                        var content = await response.Content.ReadAsStringAsync();
                        var leaderboard = JsonConvert.DeserializeObject<List<LeaderBoardEntryDto>>(content);
                        return leaderboard;
                    }
                    else
                    {
                        // Handle the unsuccessful response
                        // e.g., log error or throw an exception
                        return null;
                    }
                }
                catch (Exception ex)
                {
                    // Handle the exception
                    // e.g., log error or throw an exception
                    return null;
                }
            }
    }

}
