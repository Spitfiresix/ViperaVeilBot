using Microsoft.EntityFrameworkCore;
using GameManagerService.Models;
namespace GameManagerService.Data;

public class ApDbContext : DbContext
{
    public DbSet<Game> Game { get; set; }
    public DbSet<Rank> Rank { get; set; }
    public DbSet<Ban> Ban { get; set; }
    public DbSet<Queue> Queue { get; set; }
    public DbSet<Captain> Captain { get; set; }
    
    public ApDbContext(DbContextOptions<ApDbContext> options) : base(options)
    {
    }
}