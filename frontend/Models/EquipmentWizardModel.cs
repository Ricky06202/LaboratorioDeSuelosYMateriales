using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class EquipmentWizardModel
    {
        // LSMCH 8 Revision 2 (Verificación de Compra)
        public string FundType { get; set; } = "Funcionamiento";
        public string PurchaseOrderNo { get; set; } = "";
        public string RequestNo { get; set; } = "";
        public string ItemType { get; set; } = "Equipo de Medición"; // Used for conditional logic
        public string EquipmentName { get; set; } = "";
        public string Brand { get; set; } = "";
        public string Model { get; set; } = "";
        public string SerialNumber { get; set; } = "";
        public string Provider { get; set; } = "";
        public DateTime? ReceiveDate { get; set; } = DateTime.Today;
        public string AssignedId { get; set; } = "";
        
        // Verification Criteria (LSMCH 8 Rev 2)
        public bool Criteria1 { get; set; } = true;
        public bool Criteria2 { get; set; } = true;
        public bool Criteria3 { get; set; } = true;
        public bool Criteria4 { get; set; } = true;
        public bool Criteria5 { get; set; } = true;
        public bool Criteria6 { get; set; } = false;
        public bool Criteria7 { get; set; } = true;
        public bool Criteria8 { get; set; } = true;
        public bool Criteria9 { get; set; } = true;
        public bool Criteria10 { get; set; } = true;
        public bool Criteria11 { get; set; } = true;
        public bool Criteria12 { get; set; } = true;
        public bool Criteria13 { get; set; } = false;
        public bool Criteria14 { get; set; } = true;
        
        public string ApprovalStatus { get; set; } = "Aprobado para Uso";
        public string Observations { get; set; } = "";
        public string VerifiedBy { get; set; } = "";
        public string ReviewedBy { get; set; } = "";
        public DateTime? VerificationDate { get; set; } = DateTime.Today;
        public DateTime? ReviewDate { get; set; } = DateTime.Today;

        // LSMCH 6 Revision 1 (Registro de Adquisición)
        // Most fields are shared with LSMCH 8 Rev 2

        // LSMCH 8 (Programa de Verificación y Calibración)
        // Shared fields: Internal Inventory Number (Serial), Asset Number (N/A), Brand/Model, Equipment Name
        public string CalibrationRange { get; set; } = "N/A";
        public string CalibratedBy { get; set; } = "";
        public int CalibrationFrequency { get; set; } = 12;
        public DateTime? LastCalibrationDate { get; set; }
        public DateTime? NextCalibrationDate { get; set; }

        // LSMCH 9, 10, 11 specific fields
        public string Location { get; set; } = "AREA-1";
        public string MaintenanceMethod { get; set; } = "Manual de Fabricante";
        public string Capacity { get; set; } = "";
    }
}
