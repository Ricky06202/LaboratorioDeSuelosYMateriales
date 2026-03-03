using System;
using System.Collections.Generic;

using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class Equipo
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }
        
        [JsonPropertyName("nombre")]
        public string Nombre { get; set; } = string.Empty;
        
        [JsonPropertyName("marca")]
        public string Marca { get; set; } = string.Empty;
        
        [JsonPropertyName("modelo")]
        public string Modelo { get; set; } = string.Empty;
        
        [JsonPropertyName("numero_serie")]
        public string NumeroSerie { get; set; } = string.Empty;
        
        [JsonPropertyName("estado")]
        public string Estado { get; set; } = "Activo";
        
        [JsonPropertyName("foto_url")]
        public string? FotoUrl { get; set; }
        
        [JsonPropertyName("calibraciones")]
        public List<Calibracion> Calibraciones { get; set; } = new();
    }

    public class Calibracion
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }
        
        [JsonPropertyName("equipo_id")]
        public Guid EquipoId { get; set; }
        
        [JsonPropertyName("fecha_calibracion")]
        public DateTime FechaCalibracion { get; set; }
        
        [JsonPropertyName("fecha_vencimiento")]
        public DateTime FechaVencimiento { get; set; }
        
        [JsonPropertyName("empresa_certificadora")]
        public string EmpresaCertificadora { get; set; } = string.Empty;
        
        [JsonPropertyName("certificado_url")]
        public string? CertificadoUrl { get; set; }
    }

    public class EquipoResponse
    {
        [JsonPropertyName("items")]
        public List<Equipo> Items { get; set; } = new();
        
        [JsonPropertyName("total")]
        public int Total { get; set; }
    }

    public class EquipoCreate
    {
        [JsonPropertyName("nombre")]
        public string Nombre { get; set; } = string.Empty;
        
        [JsonPropertyName("marca")]
        public string Marca { get; set; } = string.Empty;
        
        [JsonPropertyName("modelo")]
        public string Modelo { get; set; } = string.Empty;
        
        [JsonPropertyName("numero_serie")]
        public string NumeroSerie { get; set; } = string.Empty;
        
        [JsonPropertyName("estado")]
        public string Estado { get; set; } = "Activo";
    }

    public class EquipoUpdate
    {
        [JsonPropertyName("nombre")]
        public string? Nombre { get; set; }
        
        [JsonPropertyName("marca")]
        public string? Marca { get; set; }
        
        [JsonPropertyName("modelo")]
        public string? Modelo { get; set; }
        
        [JsonPropertyName("numero_serie")]
        public string? NumeroSerie { get; set; }
        
        [JsonPropertyName("estado")]
        public string? Estado { get; set; }
        
        [JsonPropertyName("foto_url")]
        public string? FotoUrl { get; set; }
    }

    public class CalibracionCreate
    {
        [JsonPropertyName("equipo_id")]
        public Guid EquipoId { get; set; }
        
        [JsonPropertyName("fecha_calibracion")]
        public DateTime FechaCalibracion { get; set; }
        
        [JsonPropertyName("fecha_vencimiento")]
        public DateTime FechaVencimiento { get; set; }
        
        [JsonPropertyName("empresa_certificadora")]
        public string EmpresaCertificadora { get; set; } = string.Empty;
        
        [JsonPropertyName("certificado_url")]
        public string? CertificadoUrl { get; set; }
    }

    public class UploadResult
    {
        [JsonPropertyName("filename")]
        public string Filename { get; set; } = string.Empty;
    }
}
