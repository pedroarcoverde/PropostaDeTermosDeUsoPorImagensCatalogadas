using Microsoft.AspNetCore.Mvc;
using ConsentTelemetry.DTOs;
using ConsentTelemetry.Interfaces;
using ConsentTelemetry.Models;

namespace ConsentTelemetry.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ConsentController : ControllerBase
{
    private readonly IConsentRepository _consentRepository;

    public ConsentController(IConsentRepository consentRepository)
    {
        _consentRepository = consentRepository;
    }

    [HttpPost("log")]
    public async Task<IActionResult> LogConsent([FromBody] ConsentLogDto dto)
    {
        if (dto is null)
        {
            return BadRequest();
        }

        var consentRecord = new ConsentRecord
        {
            UserId = dto.UserId,
            ExperimentalGroup = dto.Group,
            HasAccepted = dto.Accepted,
            LatencyMilliseconds = dto.TimeSpentMilliseconds,
            CreatedAt = dto.Timestamp
        };

        await _consentRepository.AddAsync(consentRecord);
        return Ok(new { message = "Log de consentimento registrado." });
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ConsentRecord>>> GetAll()
    {
        var allLogs = await _consentRepository.GetAllAsync();
        return Ok(allLogs);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<ConsentRecord>> GetById(int id)
    {
        var record = await _consentRepository.GetByIdAsync(id);
        return record is null ? NotFound() : Ok(record);
    }
}
