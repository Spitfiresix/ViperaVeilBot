using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.EventArgs;
using DSharpPlus.Interactivity;
using DSharpPlus.Interactivity.Extensions;
using DSharpPlus.SlashCommands;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using snekwarselo.Commands;
using snekwarselo.Managers;
using snekwarselo.Utilities;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snekwarselo
{
    public class Bot
    {
        public DiscordClient Client { get; private set; }
        public InteractivityExtension interactivityExtension { get; private set; }
        public CommandsNextExtension commandsNextExtension { get; private set; }

        public async Task RunAsync()
        {
            var configJson = await getConfigFile();
            var config = new DiscordConfiguration()
            {
                Token = configJson.Token,
                TokenType = TokenType.Bot,
                AutoReconnect = true,
            };
            //Set the Uri for our Match Checker
            MatchCheck.Uri = configJson.Prefix;
            var client = new DiscordClient(config);
            client.UseInteractivity(new InteractivityConfiguration()
            {
                Timeout = TimeSpan.FromMinutes(2)
            });
            client.Ready += OnClientReady;
            client.ComponentInteractionCreated += OnComponentInteractionCreated;

            var commandConfig = new CommandsNextConfiguration()
            {
                StringPrefixes = new string[] { configJson.Prefix },
                EnableDms = true,
                EnableMentionPrefix = true,
            };
            var slashCommandConfig = client.UseSlashCommands(new SlashCommandsConfiguration()
            {
                Services = new ServiceCollection().AddScoped(x => new GameManagerClient(configJson.Prefix)).BuildServiceProvider()
            });

            slashCommandConfig.RegisterCommands<QueueCommands>();
            slashCommandConfig.RegisterCommands<PlayerCommand>();
            
            await client.ConnectAsync();
            await Task.Delay(-1);

        }

        private async Task OnComponentInteractionCreated(DiscordClient sender, ComponentInteractionCreateEventArgs args)
        {
            var configJson = await getConfigFile();
            var gameClient = new GameManagerClient(configJson.Prefix);

            if (args.Interaction.Data.CustomId == "1s")
            if (args.Interaction.Data.CustomId == "2s")
            if (args.Interaction.Data.CustomId == "3s")
            if (args.Interaction.Data.CustomId == "4s")
                await QueueUtilities.JoinQueue(gameClient, args.User, args.Channel, args.Interaction.Data.CustomId);
        }

        private Task OnClientReady(DiscordClient sender, ReadyEventArgs args)
        {
            MatchCheck.MatchCheckLoop(sender, args).GetAwaiter();
            return Task.CompletedTask;
        }

        private async Task<ConfigJSON> getConfigFile()
        {
            var json = string.Empty;
            var filename = "config.json";
#if DEBUG
            filename = "dev.config.json";
#endif
            using (var fs = File.OpenRead(filename))
            using (var sr = new StreamReader(fs, new UTF8Encoding(false)))
                json = await sr.ReadToEndAsync();

            var configJson = JsonConvert.DeserializeObject<ConfigJSON>(json);
           
            return configJson;
        }
    }
}
