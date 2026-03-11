using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class LabService
    {
        public int Id { get; set; }
        public string Code { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public string? Description { get; set; }
        public decimal UnitPrice { get; set; }
    }

    public class LabServiceCreate
    {
        [Required(ErrorMessage = "El código es requerido")]
        public string Code { get; set; } = string.Empty;
        
        [Required(ErrorMessage = "El nombre es requerido")]
        public string Name { get; set; } = string.Empty;
        
        public string? Description { get; set; }
        public decimal UnitPrice { get; set; }
    }

    public class LabServiceUpdate : LabServiceCreate
    {
    }
}
