public class Match
{
    public List<Player> Players { get; set; }
    public List<Player> Team1 { get; set; }
    public List<Player> Team2 { get; set; }
    public Player Captain1 { get; set; }
    public Player Captain2 { get; set; }

    public Match(List<Player> players, int mode, string teamPickMode)
    {
        Players = players;
        AssignTeams(mode, teamPickMode);
        AssignCaptains();
    }

    private void AssignTeams(int mode, string teamPickMode)
    {
        if (mode == 1)
        {
            // 1v1 mode
            Team1 = new List<Player> { Players[0] };
            Team2 = new List<Player> { Players[1] };
        }
        else if (mode == 2)
        {
            // 2v2 mode
            if (teamPickMode == "random_team")
            {
                RandomizeTeamAssignment(2);
            }
            else if (teamPickMode == "random_cap")
            {
                RandomizeCaptainAssignment(2);
                Team1 = new List<Player> { Captain1, Players[0] };
                Team2 = new List<Player> { Captain2, Players[1] };
            }
            else if (teamPickMode == "top_bottom")
            {
                Team1 = new List<Player> { Players[0], Players[1] };
                Team2 = new List<Player> { Players[2], Players[3] };
            }
            else
            {
                // Invalid team pick mode, handle accordingly
                throw new ArgumentException("Invalid team pick mode.");
            }
        }
        else if (mode == 3)
        {
            // 3v3 mode
            if (teamPickMode == "random_team")
            {
                RandomizeTeamAssignment(3);
            }
            else if (teamPickMode == "random_cap")
            {
                RandomizeCaptainAssignment(3);
                Team1 = new List<Player> { Captain1, Players[0], Players[1] };
                Team2 = new List<Player> { Captain2, Players[2], Players[3] };
            }
            else if (teamPickMode == "top_bottom")
            {
                Team1 = new List<Player> { Players[0], Players[1], Players[2] };
                Team2 = new List<Player> { Players[3], Players[4], Players[5] };
            }
            else
            {
                // Invalid team pick mode, handle accordingly
                throw new ArgumentException("Invalid team pick mode.");
            }
        }
        else if (mode == 4)
        {
            // 4v4 mode
            if (teamPickMode == "random_team")
            {
                RandomizeTeamAssignment(4);
            }
            else if (teamPickMode == "random_cap")
            {
                RandomizeCaptainAssignment(4);
                Team1 = new List<Player> { Captain1, Players[0], Players[1], Players[2] };
                Team2 = new List<Player> { Captain2, Players[3], Players[4], Players[5] };
            }
            else if (teamPickMode == "top_bottom")
            {
                Team1 = new List<Player> { Players[0], Players[1], Players[2], Players[3] };
                Team2 = new List<Player> { Players[4], Players[5], Players[6], Players[7] };
            }
            else
            {
                // Invalid team pick mode, handle accordingly
                throw new ArgumentException("Invalid team pick mode.");
            }
        }
        else
        {
            // Invalid mode, handle accordingly
            throw new ArgumentException("Invalid game mode.");
        }
    }

    private void AssignCaptains()
    {
        if (Captain1 == null)
            Captain1 = Players[0];

        if (Captain2 == null)
            Captain2 = Players[1];
    }

    private void RandomizeTeamAssignment(int teamSize)
    {
        var shuffledPlayers = Players.OrderBy(p => Guid.NewGuid()).ToList();
        Team1 = shuffledPlayers.Take(teamSize).ToList();
        Team2 = shuffledPlayers.Skip(teamSize).ToList();
    }

    private void RandomizeCaptainAssignment(int teamSize)
    {
        var shuffledPlayers = Players.OrderBy(p => Guid.NewGuid()).ToList();
        Captain1 = shuffledPlayers[0];
        Captain2 = shuffledPlayers[1];
    }
}
