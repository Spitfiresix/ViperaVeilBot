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
        return Range.Start.Value;
    }

    public int Stop()
    {
        return Range.End.Value;
    }

    public override string ToString()
    {
        return $"Name: {Name}\n" +
               $"Mode: {Mode}\n" +
               $"Url: {Url}\n" +
               $"From: {Range.Start.Value}\n" +
               $"To: {Range.End.Value}\n";
    }
}
