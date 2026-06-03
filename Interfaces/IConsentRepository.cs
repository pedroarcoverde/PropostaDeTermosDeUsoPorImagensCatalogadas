using ConsentTelemetry.Models;

namespace ConsentTelemetry.Interfaces;

public interface IConsentRepository
{
    Task AddAsync(ConsentRecord record);
    Task<List<ConsentRecord>> GetAllAsync();
    Task<ConsentRecord?> GetByIdAsync(int id);
}
