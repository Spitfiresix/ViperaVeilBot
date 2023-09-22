public class Rank
{
    public string Mode { get; }
    public string Name { get; }
    public string Url { get; }
    public Range Range { get; }

    public Rank(string mode, string name, string url, int minPoints, int maxPoints)
    {
        Mode = mode;
        Name = name;
        Url = url;
        Range = new Range(minPoints, maxPoints);
    }

    public int Start()
    {
        return Range.MinPoints;
    }

    public int Stop()
    {
        return Range.MaxPoints;
    }

    public override string ToString()
    {
        return $"Name: {Name}\n" +
               $"Mode: {Mode}\n" +
               $"Url: {Url}\n" +
               $"From: {Range.MinPoints}\n" +
               $"To: {Range.MaxPoints}\n";
    }
}

public class Range
{
    public int MinPoints { get; }
    public int MaxPoints { get; }

    public Range(int minPoints, int maxPoints)
    {
        MinPoints = minPoints;
        MaxPoints = maxPoints;
    }
}