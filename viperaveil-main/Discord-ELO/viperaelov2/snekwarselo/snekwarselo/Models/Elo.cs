namespace GameManagerService.Models
{
public class Elo
{
    public int RedAverage { get; set; }
    public int BlueAverage { get; set; }
    public int RedChanceToWin { get; set; }
    public int BlueChanceToWin { get; set; }
    public int RedRating { get; set; }
    public int BlueRating { get; set; }

    public Elo()
    {
        RedAverage = 0;
        BlueAverage = 0;
        RedChanceToWin = 0;
        BlueChanceToWin = 0;
        RedRating = 0;
        BlueRating = 0;
    }
}

}
