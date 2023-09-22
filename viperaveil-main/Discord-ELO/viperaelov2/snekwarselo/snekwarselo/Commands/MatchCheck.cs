using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using Newtonsoft.Json;
using snekwarselo.Dtos;
using snekwarselo.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace snekwarselo.Commands
{
    public static class MatchCheck
    {
        public static string Uri { get; set; }

        private static async Task<bool> CheckHasMatch()
        {
            string hasMatchUrl = $"{Uri}/has-match";
            using (HttpClient httpClient = new HttpClient())
            {
                HttpResponseMessage response = await httpClient.GetAsync(hasMatchUrl);
                if (response.IsSuccessStatusCode)
                {
                    string jsonResponse = await response.Content.ReadAsStringAsync();
                    return JsonConvert.DeserializeObject<bool>(jsonResponse);
                }
            }
            return false;
        }

        private static async Task<string> GetMatch()
        {
            string getMatchUrl = $"{Uri}/get-match";
            using (HttpClient httpClient = new HttpClient())
            {
                HttpResponseMessage response = await httpClient.GetAsync(getMatchUrl);
                if (response.IsSuccessStatusCode)
                {
                    return await response.Content.ReadAsStringAsync();
                }
            }
            return null;
        }

        private static MatchDto DeserializeMatch(string matchJson)
        {
            // Add your custom deserialization logic here
            return JsonConvert.DeserializeObject<MatchDto>(matchJson);
        }

        private static async void ProcessMatch(MatchDto matchData, DiscordClient sender)
        {
            // Add your custom processing logic here
            // Match Announcement channel
            var channel = await sender.GetChannelAsync(1109347736135933952);
            List<string> team1 = new List<string>();
            List<string> team2 = new List<string>();
            foreach(PlayerDto player in matchData.Team1)
            {
                team1.Add(player.Name);
            }
            foreach (PlayerDto player in matchData.Team2)
            {
                team2.Add(player.Name);
            }
            var redTeam = string.Join(",", team1);
            var blueTeam = string.Join(",", team2);

            DiscordEmbedBuilder embed = new DiscordEmbedBuilder()
            .WithColor(DiscordColor.Green)
            .WithTitle("Snek Wars Match")
            .WithDescription($"New Match has been found for game mode")
            .AddField("Red Team", redTeam)
            .AddField("Blue Team", blueTeam);

            DiscordMessageBuilder messageBuilder = new DiscordMessageBuilder().AddEmbed(embed)
                .AddComponents();

            await channel.SendMessageAsync(messageBuilder);
            Console.WriteLine("Match found!");
            Console.WriteLine(matchData);
            // ...
        }

        public static async Task MatchCheckLoop(DiscordClient sender, DSharpPlus.EventArgs.ReadyEventArgs e)
        {
            while (true)
            {
                bool hasMatch = await CheckHasMatch();
                if (hasMatch)
                {
                    string match = await GetMatch();
                    if (!string.IsNullOrEmpty(match))
                    {
                        MatchDto matchData = DeserializeMatch(match);
                        ProcessMatch(matchData,sender);
                    }
                }
                Thread.Sleep(5000);
            }
        }
    }
}
