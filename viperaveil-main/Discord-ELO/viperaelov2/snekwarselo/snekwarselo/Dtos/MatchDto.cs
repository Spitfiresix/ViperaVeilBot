using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snekwarselo.Dtos
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
