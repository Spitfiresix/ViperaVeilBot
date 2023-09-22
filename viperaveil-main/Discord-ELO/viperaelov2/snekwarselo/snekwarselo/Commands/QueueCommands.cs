using DSharpPlus;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using snekwarselo.Managers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;

namespace snekwarselo.Commands
{
    public class QueueCommands : ApplicationCommandModule
    {
        private GameManagerClient _gameManagerClient;
        
        public QueueCommands(GameManagerClient client)
        {
            _gameManagerClient = client;
        }
        [SlashCommand("Join Queue", "Join Matchmaking Queue")]
        public async Task JoinQueue(InteractionContext ctx)
        {

            await ctx.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Joining Queue"));
            var queueEmded = new DiscordMessageBuilder()
                .AddEmbed(new DiscordEmbedBuilder().WithTitle("Select Game mode")).AddComponents(new DiscordComponent[]{
                    CreateQueueButton("1 v 1", "1s"),
                    CreateQueueButton("2 v 2", "2s"),
                    CreateQueueButton("3 v 3", "3s"),
                    CreateQueueButton("4 v 4", "4s")
                });
                
            await ctx.Channel.SendMessageAsync(queueEmded);
        }

        [SlashCommand("Leave Queue", "Leave Matchmaking Queue")]
        public async Task LeaveQueue(InteractionContext ctx)
        {
            await ctx.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Leaving Queue"));
            var queueEmded = new DiscordMessageBuilder()
                .AddEmbed(new DiscordEmbedBuilder()
                .WithTitle("Leave MatchMaking Queue?")
                .WithDescription("Leaving Matchmaking queue can result in a penalty of 5 pts"))
                .AddComponents(new DiscordComponent[]{
                      new DiscordButtonComponent(ButtonStyle.Danger, "abort_queue", "Abort"),
                      new DiscordButtonComponent(ButtonStyle.Secondary, "cancel_queue", "Cancel")   
                }
               );

            await ctx.Channel.SendMessageAsync(queueEmded);
        }

        [SlashCommand("View Queue", "View Matchmaking Queue")]
        public async Task ViewQueue(InteractionContext ctx)
        {
            //View Queue
            //display a list of users currently in queue
        }

        private DiscordButtonComponent CreateQueueButton(string label, string gamemode)
        {
            var myButton = new DiscordButtonComponent(ButtonStyle.Primary, gamemode, label);
                return myButton;
        }
    }
}
