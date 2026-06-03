using Microsoft.EntityFrameworkCore;
using ConsentTelemetry.Interfaces;
using ConsentTelemetry.Models;

namespace ConsentTelemetry.Data;

public class ConsentRepository : IConsentRepository
{
    private readonly ConsentDbContext _dbContext;

    public ConsentRepository(ConsentDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task AddAsync(ConsentRecord record)
    {
        _dbContext.ConsentRecords.Add(record);
        await _dbContext.SaveChangesAsync();
    }

    public async Task<List<ConsentRecord>> GetAllAsync()
    {
        return await _dbContext.ConsentRecords
            .OrderByDescending(r => r.CreatedAt)
            .ToListAsync();
    }

    public async Task<ConsentRecord?> GetByIdAsync(int id)
    {
        return await _dbContext.ConsentRecords.FindAsync(id);
    }
}
