using System;
using System.ComponentModel.DataAnnotations;

namespace ConsentTelemetry.Models;

public class ConsentRecord
{
    [Key]
    public int Id { get; set; }
    public Guid UserId { get; set; }

    [Required]
    [MaxLength(20)]
    public string ExperimentalGroup { get; set; } = string.Empty;

    public bool HasAccepted { get; set; }
    public long LatencyMilliseconds { get; set; }
    public DateTime CreatedAt { get; set; }
}
