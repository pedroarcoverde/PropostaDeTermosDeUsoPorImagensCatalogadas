using Microsoft.EntityFrameworkCore;
using ConsentTelemetry.Models;

namespace ConsentTelemetry.Data;

public class ConsentDbContext : DbContext
{
    public ConsentDbContext(DbContextOptions<ConsentDbContext> options) : base(options)
    {
    }

    public DbSet<ConsentRecord> ConsentRecords => Set<ConsentRecord>();
}
