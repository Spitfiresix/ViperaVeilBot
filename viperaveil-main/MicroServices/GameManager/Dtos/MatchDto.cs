namespace GameManager.Dtos
{
    public class MatchDto
    {
        public PlayerDto[] Players { get; set; }
        public PlayerDto[] Team1 { get; set; }
        public PlayerDto[] Team2 { get; set; }
        public PlayerDto Captain1 { get; set; }
        public PlayerDto Captain2 { get; set; }
    }
}
