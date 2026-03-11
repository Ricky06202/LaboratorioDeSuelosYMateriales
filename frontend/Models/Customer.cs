using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class Customer
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string? Ruc { get; set; }
        public string? Dv { get; set; }
        public string? Email { get; set; }
        public string? Phone { get; set; }
        public string? Address { get; set; }
    }

    public class CustomerCreate
    {
        [Required(ErrorMessage = "El nombre es requerido")]
        public string Name { get; set; } = string.Empty;
        public string? Ruc { get; set; }
        public string? Dv { get; set; }
        [EmailAddress(ErrorMessage = "Email inválido")]
        public string? Email { get; set; }
        public string? Phone { get; set; }
        public string? Address { get; set; }
    }

    public class CustomerUpdate : CustomerCreate
    {
    }
}
