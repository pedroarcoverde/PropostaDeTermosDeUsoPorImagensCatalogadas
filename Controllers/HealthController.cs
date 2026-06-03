using Microsoft.AspNetCore.Mvc;

namespace ConsentTelemetry.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Get()
    {
        return Ok(new { status = "up", message = "ConsentTelemetry API is running" });
    }
}
