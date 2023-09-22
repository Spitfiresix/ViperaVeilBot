using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using snekwarselo.Managers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snekwarselo.Utilities
{
    public static class QueueUtilities
    {
        public static async Task JoinQueue(GameManagerClient client, DiscordUser user,DiscordChannel channel, string gameMode)
        {
            var player = await client.GetPlayer(user.Id.ToString());
            // if not, create user
            if (player == null)
            {
                var newPlayer = new PlayerDto
                {
                    UserId = user.Id.ToString(),
                    Name = user.Username,
                    Elo = 1000,
                    Wins = 0,
                    Losses = 0,
                };
                player.SelectedModes.Append(parseGameMode(gameMode));
                client.AddPlayer(newPlayer);
            }
            //Register for all leaderboards
            await client
                .AddPlayerToLeaderboard(player.Name,player.Elo, reverseParseGameMode(player.SelectedModes.FirstOrDefault()));
            // add user to queue
            var response = await client.EnqueuePlayer(player);
            
            if(response == QueueResponses.Success)
            {
                var embedMessage = new DiscordEmbedBuilder()
                 .WithTitle("Queue")
                 .WithDescription("You have been added to the queue")
                 .WithColor(DiscordColor.Green);

                await channel.SendMessageAsync(embed: embedMessage);
            }
            else
            {
                var embedMessage = new DiscordEmbedBuilder()
                 .WithTitle("Queue")
                 .WithDescription("You have failed to add to queue")
                 .WithColor(DiscordColor.Red);

                await channel.SendMessageAsync(embed: embedMessage);
            }

        }
        public static async Task<QueueResponses> LeaveQueue(GameManagerClient client, InteractionContext ctx)
        {
            var player = await client.GetPlayer(ctx.User.Id.ToString());
            return QueueResponses.Success;
        }

        private static int parseGameMode(string gameMode)
        {
             switch (gameMode)
            {
                case "1s":
                    return 1;
                case "2s":
                    return 2;
                case "3s":
                    return 3;
                case "4s":
                    return 4;
                default:
                    return 0;
            }
        }

        private static string reverseParseGameMode(int gameMode)
        {
            switch (gameMode)
            {
                case 1:
                    return "1s";
                case 2:
                    return "2s";
                case 3:
                    return "3s";
                case 4:
                    return "4s";
                default:
                    return "";
            }
        }

    }

}
