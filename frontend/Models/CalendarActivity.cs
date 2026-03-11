using System;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class CalendarActivity
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }
        [JsonPropertyName("title")]
        public string Title { get; set; } = string.Empty;
        [JsonPropertyName("description")]
        public string? Description { get; set; }
        [JsonPropertyName("start_date")]
        public DateTime StartDate { get; set; }
        [JsonPropertyName("end_date")]
        public DateTime? EndDate { get; set; }
        [JsonPropertyName("type")]
        public string? Type { get; set; }
        [JsonPropertyName("related_id")]
        public Guid? RelatedId { get; set; }
        [JsonPropertyName("color")]
        public string? Color { get; set; }
    }

    public class CalendarActivityCreate
    {
        [JsonPropertyName("title")]
        public string Title { get; set; } = string.Empty;
        [JsonPropertyName("description")]
        public string? Description { get; set; }
        [JsonPropertyName("start_date")]
        public DateTime StartDate { get; set; }
        [JsonPropertyName("end_date")]
        public DateTime? EndDate { get; set; }
        [JsonPropertyName("type")]
        public string? Type { get; set; }
        [JsonPropertyName("related_id")]
        public Guid? RelatedId { get; set; }
        [JsonPropertyName("color")]
        public string? Color { get; set; }
    }
}
