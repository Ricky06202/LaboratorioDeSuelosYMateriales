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
        
        [JsonPropertyName("ubicacion")]
        public string? Ubicacion { get; set; }
        
        [JsonPropertyName("fecha_proxima_calibracion")]
        public DateTime? FechaProximaCalibracion { get; set; }

        [JsonPropertyName("tipo_fondo")]
        public string? TipoFondo { get; set; }

        [JsonPropertyName("orden_compra")]
        public string? OrdenCompra { get; set; }

        [JsonPropertyName("solicitud_no")]
        public string? SolicitudNo { get; set; }

        [JsonPropertyName("tipo_bien")]
        public string? TipoBien { get; set; }

        [JsonPropertyName("fecha_recibido")]
        public DateTime? FechaRecibido { get; set; }

        [JsonPropertyName("id_asignado")]
        public string? IdAsignado { get; set; }

        [JsonPropertyName("capacidad")]
        public string? Capacidad { get; set; }

        [JsonPropertyName("ubicacion_fisica")]
        public string? UbicacionFisica { get; set; }

        [JsonPropertyName("proveedor")]
        public string? Proveedor { get; set; }

        [JsonPropertyName("estado_aprobacion")]
        public string? EstadoAprobacion { get; set; }

        [JsonPropertyName("observaciones")]
        public string? Observations { get; set; }

        [JsonPropertyName("verificado_por")]
        public string? VerificadoPor { get; set; }

        [JsonPropertyName("revisado_por")]
        public string? RevisadoPor { get; set; }

        [JsonPropertyName("fecha_verificacion")]
        public DateTime? FechaVerificacion { get; set; }

        [JsonPropertyName("fecha_revision")]
        public DateTime? FechaRevision { get; set; }

        [JsonPropertyName("rango_calibracion")]
        public string? RangoCalibracion { get; set; }

        [JsonPropertyName("frecuencia_calibracion")]
        public int? FrecuenciaCalibracion { get; set; }

        [JsonPropertyName("metodo_mantenimiento")]
        public string? MetodoMantenimiento { get; set; }

        [JsonPropertyName("criteria_1")] public bool Criteria1 { get; set; } = true;
        [JsonPropertyName("criteria_2")] public bool Criteria2 { get; set; } = true;
        [JsonPropertyName("criteria_3")] public bool Criteria3 { get; set; } = true;
        [JsonPropertyName("criteria_4")] public bool Criteria4 { get; set; } = true;
        [JsonPropertyName("criteria_5")] public bool Criteria5 { get; set; } = true;
        [JsonPropertyName("criteria_6")] public bool Criteria6 { get; set; } = false;
        [JsonPropertyName("criteria_7")] public bool Criteria7 { get; set; } = true;
        [JsonPropertyName("criteria_8")] public bool Criteria8 { get; set; } = true;
        [JsonPropertyName("criteria_9")] public bool Criteria9 { get; set; } = true;
        [JsonPropertyName("criteria_10")] public bool Criteria10 { get; set; } = true;
        [JsonPropertyName("criteria_11")] public bool Criteria11 { get; set; } = true;
        [JsonPropertyName("criteria_12")] public bool Criteria12 { get; set; } = true;
        [JsonPropertyName("criteria_13")] public bool Criteria13 { get; set; } = false;
        [JsonPropertyName("criteria_14")] public bool Criteria14 { get; set; } = true;
        
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
        
        [JsonPropertyName("ubicacion")]
        public string? Ubicacion { get; set; }

        [JsonPropertyName("tipo_fondo")]
        public string? TipoFondo { get; set; }

        [JsonPropertyName("orden_compra")]
        public string? OrdenCompra { get; set; }

        [JsonPropertyName("solicitud_no")]
        public string? SolicitudNo { get; set; }

        [JsonPropertyName("tipo_bien")]
        public string? TipoBien { get; set; }

        [JsonPropertyName("fecha_recibido")]
        public DateTime? FechaRecibido { get; set; }

        [JsonPropertyName("id_asignado")]
        public string? IdAsignado { get; set; }

        [JsonPropertyName("capacidad")]
        public string? Capacidad { get; set; }

        [JsonPropertyName("ubicacion_fisica")]
        public string? UbicacionFisica { get; set; }

        [JsonPropertyName("proveedor")]
        public string? Proveedor { get; set; }

        [JsonPropertyName("estado_aprobacion")]
        public string? EstadoAprobacion { get; set; }

        [JsonPropertyName("observaciones")]
        public string? Observations { get; set; }

        [JsonPropertyName("verificado_por")]
        public string? VerificadoPor { get; set; }

        [JsonPropertyName("revisado_por")]
        public string? RevisadoPor { get; set; }

        [JsonPropertyName("fecha_verificacion")]
        public DateTime? FechaVerificacion { get; set; }

        [JsonPropertyName("fecha_revision")]
        public DateTime? FechaRevision { get; set; }

        [JsonPropertyName("rango_calibracion")]
        public string? RangoCalibracion { get; set; }

        [JsonPropertyName("frecuencia_calibracion")]
        public int? FrecuenciaCalibracion { get; set; }

        [JsonPropertyName("metodo_mantenimiento")]
        public string? MetodoMantenimiento { get; set; }

        [JsonPropertyName("criteria_1")] public bool Criteria1 { get; set; } = true;
        [JsonPropertyName("criteria_2")] public bool Criteria2 { get; set; } = true;
        [JsonPropertyName("criteria_3")] public bool Criteria3 { get; set; } = true;
        [JsonPropertyName("criteria_4")] public bool Criteria4 { get; set; } = true;
        [JsonPropertyName("criteria_5")] public bool Criteria5 { get; set; } = true;
        [JsonPropertyName("criteria_6")] public bool Criteria6 { get; set; } = false;
        [JsonPropertyName("criteria_7")] public bool Criteria7 { get; set; } = true;
        [JsonPropertyName("criteria_8")] public bool Criteria8 { get; set; } = true;
        [JsonPropertyName("criteria_9")] public bool Criteria9 { get; set; } = true;
        [JsonPropertyName("criteria_10")] public bool Criteria10 { get; set; } = true;
        [JsonPropertyName("criteria_11")] public bool Criteria11 { get; set; } = true;
        [JsonPropertyName("criteria_12")] public bool Criteria12 { get; set; } = true;
        [JsonPropertyName("criteria_13")] public bool Criteria13 { get; set; } = false;
        [JsonPropertyName("criteria_14")] public bool Criteria14 { get; set; } = true;
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

        [JsonPropertyName("ubicacion")]
        public string? Ubicacion { get; set; }

        [JsonPropertyName("tipo_fondo")]
        public string? TipoFondo { get; set; }

        [JsonPropertyName("orden_compra")]
        public string? OrdenCompra { get; set; }

        [JsonPropertyName("solicitud_no")]
        public string? SolicitudNo { get; set; }

        [JsonPropertyName("tipo_bien")]
        public string? TipoBien { get; set; }

        [JsonPropertyName("fecha_recibido")]
        public DateTime? FechaRecibido { get; set; }

        [JsonPropertyName("id_asignado")]
        public string? IdAsignado { get; set; }

        [JsonPropertyName("capacidad")]
        public string? Capacidad { get; set; }

        [JsonPropertyName("ubicacion_fisica")]
        public string? UbicacionFisica { get; set; }

        [JsonPropertyName("proveedor")]
        public string? Proveedor { get; set; }

        [JsonPropertyName("estado_aprobacion")]
        public string? EstadoAprobacion { get; set; }

        [JsonPropertyName("observaciones")]
        public string? Observations { get; set; }

        [JsonPropertyName("verificado_por")]
        public string? VerificadoPor { get; set; }

        [JsonPropertyName("revisado_por")]
        public string? RevisadoPor { get; set; }

        [JsonPropertyName("fecha_verificacion")]
        public DateTime? FechaVerificacion { get; set; }

        [JsonPropertyName("fecha_revision")]
        public DateTime? FechaRevision { get; set; }

        [JsonPropertyName("rango_calibracion")]
        public string? RangoCalibracion { get; set; }

        [JsonPropertyName("frecuencia_calibracion")]
        public int? FrecuenciaCalibracion { get; set; }

        [JsonPropertyName("metodo_mantenimiento")]
        public string? MetodoMantenimiento { get; set; }

        [JsonPropertyName("criteria_1")] public bool? Criteria1 { get; set; }
        [JsonPropertyName("criteria_2")] public bool? Criteria2 { get; set; }
        [JsonPropertyName("criteria_3")] public bool? Criteria3 { get; set; }
        [JsonPropertyName("criteria_4")] public bool? Criteria4 { get; set; }
        [JsonPropertyName("criteria_5")] public bool? Criteria5 { get; set; }
        [JsonPropertyName("criteria_6")] public bool? Criteria6 { get; set; }
        [JsonPropertyName("criteria_7")] public bool? Criteria7 { get; set; }
        [JsonPropertyName("criteria_8")] public bool? Criteria8 { get; set; }
        [JsonPropertyName("criteria_9")] public bool? Criteria9 { get; set; }
        [JsonPropertyName("criteria_10")] public bool? Criteria10 { get; set; }
        [JsonPropertyName("criteria_11")] public bool? Criteria11 { get; set; }
        [JsonPropertyName("criteria_12")] public bool? Criteria12 { get; set; }
        [JsonPropertyName("criteria_13")] public bool? Criteria13 { get; set; }
        [JsonPropertyName("criteria_14")] public bool? Criteria14 { get; set; }
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

}
