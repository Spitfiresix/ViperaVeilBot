using Microsoft.EntityFrameworkCore;


namespace GameManagerService.Models
{
    [Keyless]
    public class Game
    {
        // Represent the game available.
        public string guildId { get; set; }
        public List<object> available_positions { get; set; }
        public Dictionary<string, object> archive { get; set; }
        public Dictionary<string, object> leaderboards { get; set; }
        public Dictionary<string, object> undecided_games { get; set; }
        public Dictionary<string, object> cancels { get; set; }
        public Dictionary<string, Queue> queues { get; set; }
        public Dictionary<string, Ban> bans { get; set; }
        public Dictionary<string, object> waiting_for_approval{ get; set; }
        public Dictionary<string, object> correctly_submitted { get; set; }
        public Dictionary<string, Dictionary<string, Rank>> ranks { get; set; } // {modeK: {nameN: RankX, nameN+1: RankY}}
        public Dictionary<string, Dictionary<string, object>> maps_archive { get; set; } // {modeK: {idN: MapX, idN+1: MapY}}
        public Dictionary<string, object> available_maps { get; set; } // {nameN: emojiN, nameK: emojiK}
        public int map_pick_mode { get; set; }
        public Elo elo { get; set; }

        // Initialize a game for a guild.
        private Game()
        {
            
        }
        public Game(string guildId)
        {
            this.guildId = guildId;
            this.available_positions = new List<object>();
            this.archive = new Dictionary<string, object>();
            this.leaderboards = new Dictionary<string, object>();
            this.undecided_games = new Dictionary<string, object>();
            this.cancels = new Dictionary<string, object>();
            this.queues = new Dictionary<string, Queue>();
            this.bans = new Dictionary<string, Ban>();
            this.waiting_for_approval = new Dictionary<string, object>();
            this.correctly_submitted = new Dictionary<string, object>();
            this.ranks = new Dictionary<string, Dictionary<string, Rank>>();
            this.maps_archive = new Dictionary<string, Dictionary<string, object>>();
            this.available_maps = new Dictionary<string, object>();
            this.map_pick_mode = 0;
            this.elo = new Elo();
        }
    }
}
