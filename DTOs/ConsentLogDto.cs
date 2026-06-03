using System;

namespace ConsentTelemetry.DTOs;

public class ConsentLogDto
{
    public Guid UserId { get; set; }
    public string Group { get; set; } = string.Empty;
    public bool Accepted { get; set; }
    public long TimeSpentMilliseconds { get; set; }
    public DateTime Timestamp { get; set; }
}
