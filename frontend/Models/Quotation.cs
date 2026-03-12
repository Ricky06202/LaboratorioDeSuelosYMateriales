using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class QuotationItem
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("quotation_id")]
        public Guid QuotationId { get; set; }

        [JsonPropertyName("item_norma")]
        public string? ItemNorma { get; set; }

        [JsonPropertyName("item_sample")]
        public string? ItemSample { get; set; }

        [JsonPropertyName("amount")]
        public int Amount { get; set; } = 1;

        [JsonPropertyName("description")]
        public string? Description { get; set; }

        [JsonPropertyName("unit_price")]
        public decimal UnitPrice { get; set; }

        [JsonPropertyName("total_price")]
        public decimal TotalPrice { get; set; }
    }

    public class Quotation
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }

        [JsonPropertyName("quotation_number")]
        public string QuotationNumber { get; set; } = string.Empty;

        [JsonPropertyName("year")]
        public int Year { get; set; }

        [JsonPropertyName("date")]
        public DateTime Date { get; set; }

        [JsonPropertyName("customer_id")]
        public Guid? CustomerId { get; set; }

        [JsonPropertyName("customer_order_id")]
        public Guid? CustomerOrderId { get; set; }

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("client_email")]
        public string? ClientEmail { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_ruc")]
        public string? ProjectRuc { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("mobilization_cost")]
        public decimal MobilizationCost { get; set; }

        [JsonPropertyName("viatics_cost")]
        public decimal ViaticsCost { get; set; }

        [JsonPropertyName("subtotal_amount")]
        public decimal SubtotalAmount { get; set; }

        [JsonPropertyName("total_amount")]
        public decimal TotalAmount { get; set; }

        [JsonPropertyName("note")]
        public string? Note { get; set; }

        [JsonPropertyName("created_by")]
        public string? CreatedBy { get; set; }

        [JsonPropertyName("items")]
        public List<QuotationItem> Items { get; set; } = new();
    }

    public class QuotationItemCreate
    {
        [JsonPropertyName("item_norma")]
        public string? ItemNorma { get; set; }

        [JsonPropertyName("item_sample")]
        public string? ItemSample { get; set; }

        [JsonPropertyName("amount")]
        public int Amount { get; set; } = 1;

        [JsonPropertyName("description")]
        public string? Description { get; set; }

        [JsonPropertyName("unit_price")]
        public decimal UnitPrice { get; set; }
    }

    public class QuotationCreate
    {
        [JsonPropertyName("customer_id")]
        public Guid? CustomerId { get; set; }

        [JsonPropertyName("customer_order_id")]
        public Guid? CustomerOrderId { get; set; }

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("client_email")]
        public string? ClientEmail { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_ruc")]
        public string? ProjectRuc { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("mobilization_cost")]
        public decimal MobilizationCost { get; set; }

        [JsonPropertyName("viatics_cost")]
        public decimal ViaticsCost { get; set; }

        [JsonPropertyName("note")]
        public string? Note { get; set; }

        [JsonPropertyName("items")]
        public List<QuotationItemCreate> Items { get; set; } = new();
    }
}
