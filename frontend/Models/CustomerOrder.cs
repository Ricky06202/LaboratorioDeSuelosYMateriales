using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class CustomerOrderItem
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("customer_order_id")]
        public Guid CustomerOrderId { get; set; }

        [JsonPropertyName("item_number")]
        public int? ItemNumber { get; set; }

        [JsonPropertyName("test_name")]
        public string? TestName { get; set; }

        [JsonPropertyName("sample_type")]
        public string? SampleType { get; set; }

        [JsonPropertyName("test_count")]
        public int TestCount { get; set; } = 1;

        [JsonPropertyName("norm_method")]
        public string? NormMethod { get; set; }
    }

    public class CustomerOrder
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }

        [JsonPropertyName("order_number")]
        public string OrderNumber { get; set; } = string.Empty;

        [JsonPropertyName("date")]
        public DateTime Date { get; set; }

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_dv")]
        public string? ClientDv { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_responsable_phone")]
        public string? ProjectResponsablePhone { get; set; }

        [JsonPropertyName("project_responsable_email")]
        public string? ProjectResponsableEmail { get; set; }

        [JsonPropertyName("observations")]
        public string? Observations { get; set; }

        [JsonPropertyName("attended_by")]
        public string? AttendedBy { get; set; }

        [JsonPropertyName("approved_quotation_number")]
        public string? ApprovedQuotationNumber { get; set; }

        [JsonPropertyName("created_by")]
        public string? CreatedBy { get; set; }

        [JsonPropertyName("items")]
        public List<CustomerOrderItem> Items { get; set; } = new();
    }

    public class CustomerOrderItemCreate
    {
        [JsonPropertyName("item_number")]
        public int? ItemNumber { get; set; }

        [JsonPropertyName("test_name")]
        public string? TestName { get; set; }

        [JsonPropertyName("sample_type")]
        public string? SampleType { get; set; }

        [JsonPropertyName("test_count")]
        public int TestCount { get; set; } = 1;

        [JsonPropertyName("norm_method")]
        public string? NormMethod { get; set; }
    }

    public class CustomerOrderCreate
    {
        [JsonPropertyName("date")]
        public DateTime Date { get; set; } = DateTime.Today;

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_dv")]
        public string? ClientDv { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_responsable_phone")]
        public string? ProjectResponsablePhone { get; set; }

        [JsonPropertyName("project_responsable_email")]
        public string? ProjectResponsableEmail { get; set; }

        [JsonPropertyName("observations")]
        public string? Observations { get; set; }

        [JsonPropertyName("attended_by")]
        public string? AttendedBy { get; set; }

        [JsonPropertyName("approved_quotation_number")]
        public string? ApprovedQuotationNumber { get; set; }

        [JsonPropertyName("items")]
        public List<CustomerOrderItemCreate> Items { get; set; } = new();
    }
}
