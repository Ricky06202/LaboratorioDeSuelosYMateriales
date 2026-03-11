using System;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class LabService
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }
        [JsonPropertyName("code")]
        public string Code { get; set; } = string.Empty;
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
        [JsonPropertyName("description")]
        public string? Description { get; set; }
        [JsonPropertyName("unit_price")]
        public decimal UnitPrice { get; set; }
    }

    public class LabServiceCreate
    {
        [Required(ErrorMessage = "El código es requerido")]
        [JsonPropertyName("code")]
        public string Code { get; set; } = string.Empty;
        
        [Required(ErrorMessage = "El nombre es requerido")]
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
        
        [JsonPropertyName("description")]
        public string? Description { get; set; }
        [JsonPropertyName("unit_price")]
        public decimal UnitPrice { get; set; }
    }

    public class LabServiceUpdate : LabServiceCreate
    {
    }
}
