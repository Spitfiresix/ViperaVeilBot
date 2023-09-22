using DSharpPlus;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using snekwarselo.Managers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snekwarselo.Commands
{
    public class PlayerCommand : ApplicationCommandModule
    {
        private GameManagerClient _gameManagerClient;

        public PlayerCommand(GameManagerClient client)
        {
            _gameManagerClient = client;
        }
        //Get Player
        [SlashCommand("Player", "Get Player Card")]
        public async Task Player(InteractionContext ctx, [Option("player","player card to get" )] DiscordUser user )
        {
            await ctx.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Fetching Player..."));

            var player = await _gameManagerClient.GetPlayer(user.Id.ToString());
            if (player == null)
            {
                var embedMessage = new DiscordEmbedBuilder()
                    .WithTitle("Player")
                    .WithDescription("Player not found")
                    .WithColor(DiscordColor.Red);

                await ctx.Channel.SendMessageAsync(embed: embedMessage);
                return;
            }

            //Build Player Card
            var playerEmbed = new DiscordEmbedBuilder()
                .WithThumbnail(user.AvatarUrl)
                .WithTitle(player.Name)
                .WithDescription("Win rate :" +  player.WinLossRatio)
                .WithDescription("Matches Played :" +  player.MatchesPlayed)
                .WithDescription("Elo :" +  player.Elo)
                .WithDescription("Losses :" +  player.Losses)
                .WithDescription("Wins :" + player.Wins)
                .WithColor(DiscordColor.Green);

            await ctx.Channel.SendMessageAsync (embed: playerEmbed);
            await Task.CompletedTask;
        }

        [SlashCommand("Add Player", "Add Player")]
        public async Task AddPlayer(InteractionContext ctx)
        {
            await ctx.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Adding Player..."));
            var player = await _gameManagerClient.GetPlayer(ctx.User.Id.ToString());
            // if not, create user
            if (player == null)
            {
                var newPlayer = new PlayerDto
                {
                    UserId = ctx.User.Id.ToString(),
                    Name = ctx.User.Username,
                    Elo = 1000,
                    Wins = 0,
                    Losses = 0,
                };

                var response = await _gameManagerClient.AddPlayer(newPlayer);
                if (response)
                {
                    var playerEmbed = new DiscordEmbedBuilder()
                            .WithTitle("Player")
                            .WithDescription("Player Created")
                            .WithColor(DiscordColor.Green);
                    await ctx.Channel.SendMessageAsync(embed: playerEmbed);
                    await Task.CompletedTask;
                }
                else 
                {
                    var playerEmbed = new DiscordEmbedBuilder()
                               .WithTitle("Player")
                               .WithDescription("Player Creation Failed")
                               .WithColor(DiscordColor.Red);
                    await ctx.Channel.SendMessageAsync(embed: playerEmbed);
                    await Task.CompletedTask;
                }
            }
            else
            {
                var embed = new DiscordEmbedBuilder()
                  .WithTitle("Player")
                  .WithDescription("Player Exists")
                  .WithColor(DiscordColor.Green);
                await ctx.Channel.SendMessageAsync(embed: embed);
                await Task.CompletedTask;
            }
        }

    }
}
