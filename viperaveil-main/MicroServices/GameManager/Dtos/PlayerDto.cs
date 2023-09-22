
    public class PlayerDto
    {
        public int UserId { get; set; }
        public string Name { get; set; }

        public int Wins { get; set; }

        public int Losses { get; set; }

        public int MatchesPlayed => Wins + Losses;

        public double WinLossRatio => (double)Wins / MatchesPlayed;

        public int Elo { get; set; }

        public int HighestElo { get; set; }

        public int LongestWinstreak { get; set; }

        public int LongestLossstreak { get; set; }

        public int CurrentWinstreak { get; set; }

        public int CurrentLossstreak { get; set; }
        public int[] SelectedModes { get; set;}
    }