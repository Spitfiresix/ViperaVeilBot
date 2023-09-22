using System;
using System.Collections.Generic;

public class Queue
{
    public List<Player> Players { get; set; }
    public List<Player> RedTeam { get; set; }
    public List<Player> BlueTeam { get; set; }
    public int MaxQueue { get; set; }
    public bool HasQueueBeenFull { get; set; }
    public int Mode { get; set; }
    public int MapMode { get; set; }
    public HashSet<int> Reacted { get; set; }
    public int GameId { get; set; }

    public Queue(int maxQueue, int mode, int mapMode, int lastId = 0)
    {
        if (maxQueue < 2 || maxQueue % 2 == 1)
        {
            throw new ArgumentException("The max queue must be an even number >= 2");
        }

        Players = new List<Player>();
        RedTeam = new List<Player>();
        BlueTeam = new List<Player>();
        MaxQueue = maxQueue;
        HasQueueBeenFull = false;
        Mode = mode;
        MapMode = mapMode;
        Reacted = new HashSet<int> { 0 };
        GameId = lastId + 1;
    }
}