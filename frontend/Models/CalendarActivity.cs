using System;

namespace frontend.Models
{
    public class CalendarActivity
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string? Description { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? Type { get; set; }
        public Guid? RelatedId { get; set; }
        public string? Color { get; set; }
    }

    public class CalendarActivityCreate
    {
        public string Title { get; set; } = string.Empty;
        public string? Description { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? Type { get; set; }
        public Guid? RelatedId { get; set; }
        public string? Color { get; set; }
    }
}
