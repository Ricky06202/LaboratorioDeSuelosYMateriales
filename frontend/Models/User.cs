using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class Permission
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;

        [JsonPropertyName("code")]
        public string Code { get; set; } = string.Empty;
    }

    public class Role
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;

        [JsonPropertyName("permissions")]
        public List<Permission> Permissions { get; set; } = new();
    }

    public class User
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("full_name")]
        public string FullName { get; set; } = string.Empty;

        [JsonPropertyName("phone")]
        public string? Phone { get; set; }

        [JsonPropertyName("cell_phone")]
        public string? CellPhone { get; set; }

        [JsonPropertyName("birth_date")]
        public DateTime? BirthDate { get; set; }

        [JsonPropertyName("cedula")]
        public string? Cedula { get; set; }

        [JsonPropertyName("linkedin")]
        public string? Linkedin { get; set; }

        [JsonPropertyName("is_active")]
        public bool IsActive { get; set; } = true;

        [JsonPropertyName("roles")]
        public List<Role> Roles { get; set; } = new();

        public string RoleNames => Roles != null && Roles.Any() 
            ? string.Join(", ", Roles.Select(r => r.Name)) 
            : "Sin Rol";
            
        public bool HasPermission(string code) => 
            Roles?.Any(r => r.Permissions?.Any(p => p.Code == code) == true) == true;
    }

    public class UserCreate
    {
        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("password")]
        public string Password { get; set; } = string.Empty;

        [JsonPropertyName("full_name")]
        public string FullName { get; set; } = string.Empty;

        [JsonPropertyName("role_ids")]
        public List<int> RoleIds { get; set; } = new();
    }

    public class UserUpdate
    {
        [JsonPropertyName("email")]
        public string? Email { get; set; }

        [JsonPropertyName("password")]
        public string? Password { get; set; }

        [JsonPropertyName("full_name")]
        public string? FullName { get; set; }

        [JsonPropertyName("phone")]
        public string? Phone { get; set; }

        [JsonPropertyName("cell_phone")]
        public string? CellPhone { get; set; }

        [JsonPropertyName("birth_date")]
        public DateTime? BirthDate { get; set; }

        [JsonPropertyName("cedula")]
        public string? Cedula { get; set; }

        [JsonPropertyName("linkedin")]
        public string? Linkedin { get; set; }

        [JsonPropertyName("role_ids")]
        public List<int>? RoleIds { get; set; }

        [JsonPropertyName("is_active")]
        public bool? IsActive { get; set; }
    }

    public class ProfileUpdate
    {
        [JsonPropertyName("full_name")]
        public string? FullName { get; set; }

        [JsonPropertyName("phone")]
        public string? Phone { get; set; }

        [JsonPropertyName("cell_phone")]
        public string? CellPhone { get; set; }

        [JsonPropertyName("birth_date")]
        public DateTime? BirthDate { get; set; }

        [JsonPropertyName("cedula")]
        public string? Cedula { get; set; }

        [JsonPropertyName("linkedin")]
        public string? Linkedin { get; set; }
    }

    public class PasswordChange
    {
        [JsonPropertyName("current_password")]
        public string CurrentPassword { get; set; } = string.Empty;

        [JsonPropertyName("new_password")]
        public string NewPassword { get; set; } = string.Empty;

        [JsonPropertyName("confirm_password")]
        public string ConfirmPassword { get; set; } = string.Empty;
    }

    public class RoleCreate
    {
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;

        [JsonPropertyName("permission_ids")]
        public List<int> PermissionIds { get; set; } = new();
    }
}
