using System.Net.Http.Json;
using System.Net.Http.Headers;
using Microsoft.JSInterop;
using frontend.Models;

namespace frontend.Services
{
    public class UserService
    {
        private readonly HttpClient _httpClient;
        private readonly IJSRuntime _jsRuntime;

        public UserService(HttpClient httpClient, IJSRuntime jsRuntime)
        {
            _httpClient = httpClient;
            _jsRuntime = jsRuntime;
        }

        public async Task<List<User>> GetUsersAsync()
        {
            await SetAuthorizationHeaderAsync();
            return await _httpClient.GetFromJsonAsync<List<User>>("api/usuarios/", AppJsonSerializerContext.Default.ListUser) ?? new();
        }

        public async Task<User> CreateUserAsync(UserCreate user)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PostAsJsonAsync("api/usuarios/", user, AppJsonSerializerContext.Default.UserCreate);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<User>(AppJsonSerializerContext.Default.User) ?? new();
        }

        public async Task<User> UpdateUserAsync(int userId, UserUpdate user)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PutAsJsonAsync($"api/usuarios/{userId}", user, AppJsonSerializerContext.Default.UserUpdate);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<User>(AppJsonSerializerContext.Default.User) ?? new();
        }

        public async Task DeleteUserAsync(int userId)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.DeleteAsync($"api/usuarios/{userId}");
            await EnsureSuccessOrThrowAsync(response);
        }

        public async Task<List<Role>> GetRolesAsync()
        {
            await SetAuthorizationHeaderAsync();
            return await _httpClient.GetFromJsonAsync<List<Role>>("api/usuarios/roles", AppJsonSerializerContext.Default.ListRole) ?? new();
        }

        public async Task<List<Permission>> GetPermissionsAsync()
        {
            await SetAuthorizationHeaderAsync();
            return await _httpClient.GetFromJsonAsync<List<Permission>>("api/usuarios/permissions", AppJsonSerializerContext.Default.ListPermission) ?? new();
        }

        public async Task<Role> CreateRoleAsync(string name, List<int> permissionIds)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PostAsJsonAsync("api/usuarios/roles", new RoleCreate { Name = name, PermissionIds = permissionIds }, AppJsonSerializerContext.Default.RoleCreate);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Role>(AppJsonSerializerContext.Default.Role) ?? new();
        }

        public async Task<Role> UpdateRoleAsync(int roleId, string name, List<int> permissionIds)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PutAsJsonAsync($"api/usuarios/roles/{roleId}", new RoleCreate { Name = name, PermissionIds = permissionIds }, AppJsonSerializerContext.Default.RoleCreate);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Role>(AppJsonSerializerContext.Default.Role) ?? new();
        }

        public async Task DeleteRoleAsync(int roleId)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.DeleteAsync($"api/usuarios/roles/{roleId}");
            await EnsureSuccessOrThrowAsync(response);
        }

        private async Task SetAuthorizationHeaderAsync()
        {
            var token = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", "authToken");
            if (!string.IsNullOrWhiteSpace(token))
            {
                _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            }
        }

        private async Task EnsureSuccessOrThrowAsync(HttpResponseMessage response)
        {
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                try
                {
                    using var doc = System.Text.Json.JsonDocument.Parse(content);
                    if (doc.RootElement.TryGetProperty("error", out var errorProp))
                    {
                        throw new Exception(errorProp.GetString());
                    }
                    if (doc.RootElement.TryGetProperty("detail", out var detailProp))
                    {
                        if (detailProp.ValueKind == System.Text.Json.JsonValueKind.String)
                            throw new Exception(detailProp.GetString());
                        else
                            throw new Exception("Error de validación en el servidor.");
                    }
                }
                catch (Exception ex) when (ex is not Exception) { }
                
                throw new Exception($"Error {response.StatusCode}: {content}");
            }
        }
    }
}
