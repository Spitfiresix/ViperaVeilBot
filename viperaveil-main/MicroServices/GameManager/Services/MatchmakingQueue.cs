using System;
using System.Collections.Generic;

public class MatchmakingQueue
{
    private Dictionary<int, Queue<Player>> queuesByMode;
    private Queue<Player> globalQueue;

    public MatchmakingQueue()
    {
        queuesByMode = new Dictionary<int, Queue<Player>>();
        globalQueue = new Queue<Player>();
    }

    public void Enqueue(Player player, List<int> modes)
    {
        if (modes.Count == 0)
        {
            Console.WriteLine($"Player {player.Name} has not selected any modes to join.");
            return;
        }

        foreach (int mode in modes)
        {
            if (!queuesByMode.ContainsKey(mode))
            {
                queuesByMode[mode] = new Queue<Player>();
            }

            queuesByMode[mode].Enqueue(player);
        }

        globalQueue.Enqueue(player);
        Console.WriteLine($"Player {player.Name} has been added to the global queue with selected modes.");
    }

    public void Dequeue()
    {
        if (globalQueue.Count == 0)
        {
            Console.WriteLine("No players in the global queue.");
            return;
        }

        Player player = globalQueue.Dequeue();
        int matchedMode = GetNextAvailableMode(player);

        if (matchedMode != -1)
        {
            queuesByMode[matchedMode].Dequeue();
            Console.WriteLine($"Player {player.Name} has been matched in the {GetModeName(matchedMode)} game mode.");
        }
        else
        {
            Console.WriteLine($"No available match found for player {player.Name}.");
        }
    }

    private int GetNextAvailableMode(Player player)
    {
        // Sort the selected modes in descending order based on team size
        var sortedModes = player.SelectedModes.OrderByDescending(mode => mode).ToList();

        foreach (int mode in sortedModes)
        {
            if (queuesByMode.ContainsKey(mode) && queuesByMode[mode].Count > 0)
            {
                return mode;
            }
        }
        return -1;
    }

    private string GetModeName(int mode)
    {
        switch (mode)
        {
            case 1:
                return "1s";
            case 2:
                return "2s";
            case 3:
                return "3s";
            default:
                return "Unknown";
        }
    }

public bool HasMatch(out int matchedMode, out List<Player> matchedPlayers)
{
    matchedMode = -1;
    matchedPlayers = null;

    foreach (var modeQueue in queuesByMode)
    {
        int mode = modeQueue.Key;
        Queue<Player> queue = modeQueue.Value;

        if (queue.Count >= 2)
        {
            int requiredPlayers = GetRequiredPlayersForMode(mode);

            if (queue.Count >= requiredPlayers)
            {
                matchedMode = mode;
                matchedPlayers = new List<Player>();

                for (int i = 0; i < requiredPlayers; i++)
                {
                    matchedPlayers.Add(queue.Dequeue());
                }

                return true;
            }
        }
    }

    return false;
}

private int GetRequiredPlayersForMode(int mode)
{
    switch (mode)
    {
        case 1:
            return 2;
        case 2:
            return 4;
        case 3:
            return 6;
        default:
            return 0;
    }
}

public List<Player> GetMatchedPlayers(int mode)
{
    if (queuesByMode.ContainsKey(mode))
    {
        return queuesByMode[mode].ToList();
    }

    return new List<Player>();
}

public int GetModeForQueue(Queue<Player> queue)
{
    foreach (var modeQueue in queuesByMode)
    {
        if (modeQueue.Value == queue)
        {
            return modeQueue.Key;
        }
    }

    return -1;
}


}

