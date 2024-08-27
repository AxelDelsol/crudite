using Microsoft.EntityFrameworkCore;

namespace Crudite.Models;

public class TeaContext : DbContext
{
    public TeaContext(DbContextOptions options) : base(options)
    {
    }

    public DbSet<Tea> Teas { get; set; }
}
