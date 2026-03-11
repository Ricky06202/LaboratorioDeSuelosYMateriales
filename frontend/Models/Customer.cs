using System;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class Customer
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
        [JsonPropertyName("ruc")]
        public string? Ruc { get; set; }
        [JsonPropertyName("dv")]
        public string? Dv { get; set; }
        [JsonPropertyName("email")]
        public string? Email { get; set; }
        [JsonPropertyName("phone")]
        public string? Phone { get; set; }
        [JsonPropertyName("address")]
        public string? Address { get; set; }
    }

    public class CustomerCreate
    {
        [Required(ErrorMessage = "El nombre es requerido")]
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
        [JsonPropertyName("ruc")]
        public string? Ruc { get; set; }
        [JsonPropertyName("dv")]
        public string? Dv { get; set; }
        [EmailAddress(ErrorMessage = "Email inválido")]
        [JsonPropertyName("email")]
        public string? Email { get; set; }
        [JsonPropertyName("phone")]
        public string? Phone { get; set; }
        [JsonPropertyName("address")]
        public string? Address { get; set; }
    }

    public class CustomerUpdate : CustomerCreate
    {
    }
}
