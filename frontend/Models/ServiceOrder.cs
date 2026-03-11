using System;
using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class ServiceOrder
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }

        [JsonPropertyName("order_number")]
        public string OrderNumber { get; set; } = string.Empty;

        [JsonPropertyName("year")]
        public int Year { get; set; }

        [JsonPropertyName("date")]
        public DateTime Date { get; set; }

        [JsonPropertyName("customer_id")]
        public Guid? CustomerId { get; set; }

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_dv")]
        public string? ClientDv { get; set; }

        [JsonPropertyName("quotation_ref")]
        public string? QuotationRef { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("client_email")]
        public string? ClientEmail { get; set; }

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_phone")]
        public string? ProjectPhone { get; set; }

        [JsonPropertyName("service_type_ensayos")]
        public bool ServiceTypeEnsayos { get; set; } = true;

        [JsonPropertyName("service_type_muestreo")]
        public bool ServiceTypeMuestreo { get; set; } = false;

        [JsonPropertyName("performed_by_laboratory")]
        public bool PerformedByLaboratory { get; set; } = true;

        [JsonPropertyName("performed_by_client")]
        public bool PerformedByClient { get; set; } = false;

        [JsonPropertyName("performed_by_inspection")]
        public bool PerformedByInspection { get; set; } = false;

        [JsonPropertyName("item_description")]
        public string? ItemDescription { get; set; }

        [JsonPropertyName("methodology")]
        public string? Methodology { get; set; }

        [JsonPropertyName("subcontraction")]
        public bool Subcontraction { get; set; } = false;

        [JsonPropertyName("subcontraction_details")]
        public string? SubcontractionDetails { get; set; }

        [JsonPropertyName("request_declaration_conformity")]
        public bool RequestDeclarationConformity { get; set; } = false;

        [JsonPropertyName("declaration_specification")]
        public string? DeclarationSpecification { get; set; }

        [JsonPropertyName("decision_rule_not_applicable")]
        public bool DecisionRuleNotApplicable { get; set; } = true;

        [JsonPropertyName("decision_rule_client_agreed")]
        public bool DecisionRuleClientAgreed { get; set; } = false;

        [JsonPropertyName("decision_rule_inherent")]
        public bool DecisionRuleInherent { get; set; } = false;

        [JsonPropertyName("client_deviation")]
        public bool ClientDeviation { get; set; } = false;

        [JsonPropertyName("deviation_details")]
        public string? DeviationDetails { get; set; }

        [JsonPropertyName("observations")]
        public string? Observations { get; set; }

        [JsonPropertyName("sample_conservation_time")]
        public int SampleConservationTime { get; set; } = 30;

        [JsonPropertyName("total_cost")]
        public decimal TotalCost { get; set; }

        [JsonPropertyName("paid_100_percent")]
        public bool Paid100Percent { get; set; } = false;

        [JsonPropertyName("service_sale_receipt_number")]
        public string? ServiceSaleReceiptNumber { get; set; }

        [JsonPropertyName("relates_to_inform")]
        public string? RelatesToInform { get; set; }

        [JsonPropertyName("number_of_informs")]
        public int NumberOfInforms { get; set; } = 1;

        [JsonPropertyName("support_institutional")]
        public bool SupportInstitutional { get; set; } = false;

        [JsonPropertyName("related_document")]
        public string? RelatedDocument { get; set; }

        [JsonPropertyName("attended_by")]
        public string? AttendedBy { get; set; }

        [JsonPropertyName("applicant_name")]
        public string? ApplicantName { get; set; }

        [JsonPropertyName("applicant_id_number")]
        public string? ApplicantIdNumber { get; set; }

        [JsonPropertyName("created_by")]
        public string? CreatedBy { get; set; }
    }

    public class ServiceOrderCreate
    {
        [JsonPropertyName("customer_id")]
        public Guid? CustomerId { get; set; }

        [JsonPropertyName("client_name")]
        public string ClientName { get; set; } = string.Empty;

        [JsonPropertyName("client_ruc")]
        public string? ClientRuc { get; set; }

        [JsonPropertyName("client_dv")]
        public string? ClientDv { get; set; }

        [JsonPropertyName("quotation_ref")]
        public string? QuotationRef { get; set; }

        [JsonPropertyName("client_phone")]
        public string? ClientPhone { get; set; }

        [JsonPropertyName("client_email")]
        public string? ClientEmail { get; set; }

        [JsonPropertyName("client_direction")]
        public string? ClientDirection { get; set; }

        [JsonPropertyName("project_name")]
        public string? ProjectName { get; set; }

        [JsonPropertyName("project_location")]
        public string? ProjectLocation { get; set; }

        [JsonPropertyName("project_responsable")]
        public string? ProjectResponsable { get; set; }

        [JsonPropertyName("project_phone")]
        public string? ProjectPhone { get; set; }

        [JsonPropertyName("service_type_ensayos")]
        public bool ServiceTypeEnsayos { get; set; } = true;

        [JsonPropertyName("service_type_muestreo")]
        public bool ServiceTypeMuestreo { get; set; } = false;

        [JsonPropertyName("performed_by_laboratory")]
        public bool PerformedByLaboratory { get; set; } = true;

        [JsonPropertyName("performed_by_client")]
        public bool PerformedByClient { get; set; } = false;

        [JsonPropertyName("performed_by_inspection")]
        public bool PerformedByInspection { get; set; } = false;

        [JsonPropertyName("item_description")]
        public string? ItemDescription { get; set; }

        [JsonPropertyName("methodology")]
        public string? Methodology { get; set; }

        [JsonPropertyName("subcontraction")]
        public bool Subcontraction { get; set; } = false;

        [JsonPropertyName("subcontraction_details")]
        public string? SubcontractionDetails { get; set; }

        [JsonPropertyName("request_declaration_conformity")]
        public bool RequestDeclarationConformity { get; set; } = false;

        [JsonPropertyName("declaration_specification")]
        public string? DeclarationSpecification { get; set; }

        [JsonPropertyName("decision_rule_not_applicable")]
        public bool DecisionRuleNotApplicable { get; set; } = true;

        [JsonPropertyName("decision_rule_client_agreed")]
        public bool DecisionRuleClientAgreed { get; set; } = false;

        [JsonPropertyName("decision_rule_inherent")]
        public bool DecisionRuleInherent { get; set; } = false;

        [JsonPropertyName("client_deviation")]
        public bool ClientDeviation { get; set; } = false;

        [JsonPropertyName("deviation_details")]
        public string? DeviationDetails { get; set; }

        [JsonPropertyName("observations")]
        public string? Observations { get; set; }

        [JsonPropertyName("sample_conservation_time")]
        public int SampleConservationTime { get; set; } = 30;

        [JsonPropertyName("total_cost")]
        public decimal TotalCost { get; set; }

        [JsonPropertyName("paid_100_percent")]
        public bool Paid100Percent { get; set; } = false;

        [JsonPropertyName("service_sale_receipt_number")]
        public string? ServiceSaleReceiptNumber { get; set; }

        [JsonPropertyName("relates_to_inform")]
        public string? RelatesToInform { get; set; }

        [JsonPropertyName("number_of_informs")]
        public int NumberOfInforms { get; set; } = 1;

        [JsonPropertyName("support_institutional")]
        public bool SupportInstitutional { get; set; } = false;

        [JsonPropertyName("related_document")]
        public string? RelatedDocument { get; set; }

        [JsonPropertyName("attended_by")]
        public string? AttendedBy { get; set; }

        [JsonPropertyName("applicant_name")]
        public string? ApplicantName { get; set; }

        [JsonPropertyName("applicant_id_number")]
        public string? ApplicantIdNumber { get; set; }
    }
}
