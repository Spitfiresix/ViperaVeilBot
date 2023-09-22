public class Captain
{
    public int TimeLeft { get; set; }
    public object LastActivity { get; set; }
    public object Timeout { get; set; }

    public Captain(int timeLeft)
    {
        TimeLeft = timeLeft;
    }
}
