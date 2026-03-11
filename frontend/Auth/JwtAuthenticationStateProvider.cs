using System.Security.Claims;
using System.Text.Json;
using Microsoft.AspNetCore.Components.Authorization;
using Microsoft.JSInterop;
using frontend.Models;

namespace frontend.Auth
{
    public class JwtAuthenticationStateProvider : AuthenticationStateProvider
    {
        private readonly IJSRuntime _jsRuntime;
        private const string TokenKey = "authToken";

        public JwtAuthenticationStateProvider(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime;
        }

        public override async Task<AuthenticationState> GetAuthenticationStateAsync()
        {
            try
            {
                var token = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", TokenKey);

                if (string.IsNullOrWhiteSpace(token))
                {
                    return new AuthenticationState(new ClaimsPrincipal(new ClaimsIdentity()));
                }

                return new AuthenticationState(new ClaimsPrincipal(new ClaimsIdentity(ParseClaimsFromJwt(token), "jwt")));
            }
            catch (InvalidOperationException)
            {
                return new AuthenticationState(new ClaimsPrincipal(new ClaimsIdentity()));
            }
        }

        public async Task MarkUserAsAuthenticated(string token)
        {
            await _jsRuntime.InvokeVoidAsync("localStorage.setItem", TokenKey, token);
            var authenticatedUser = new ClaimsPrincipal(new ClaimsIdentity(ParseClaimsFromJwt(token), "jwt"));
            var authState = Task.FromResult(new AuthenticationState(authenticatedUser));
            NotifyAuthenticationStateChanged(authState);
        }

        public async Task MarkUserAsLoggedOut()
        {
            await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", TokenKey);
            var anonymousUser = new ClaimsPrincipal(new ClaimsIdentity());
            var authState = Task.FromResult(new AuthenticationState(anonymousUser));
            NotifyAuthenticationStateChanged(authState);
        }

        private IEnumerable<Claim> ParseClaimsFromJwt(string jwt)
        {
            var claims = new List<Claim>();
            var payload = jwt.Split('.')[1];
            var jsonBytes = ParseBase64WithoutPadding(payload);
            var keyValuePairs = JsonSerializer.Deserialize<Dictionary<string, object>>(jsonBytes, AppJsonSerializerContext.Default.DictionaryStringObject);

            if (keyValuePairs != null)
            {
                // 1. Roles
                keyValuePairs.TryGetValue(ClaimTypes.Role, out object? roles);
                if (roles != null)
                {
                    var rolesString = roles.ToString();
                    if (rolesString != null && rolesString.Trim().StartsWith("["))
                    {
                        var parsedRoles = JsonSerializer.Deserialize<string[]>(rolesString, AppJsonSerializerContext.Default.StringArray);
                        if (parsedRoles != null)
                        {
                            foreach (var parsedRole in parsedRoles)
                            {
                                claims.Add(new Claim(ClaimTypes.Role, parsedRole));
                            }
                        }
                    }
                    else
                    {
                        claims.Add(new Claim(ClaimTypes.Role, rolesString ?? string.Empty));
                    }
                    keyValuePairs.Remove(ClaimTypes.Role);
                }

                // 2. Permissions
                keyValuePairs.TryGetValue("permissions", out object? permissions);
                if (permissions != null)
                {
                    var permissionsString = permissions.ToString();
                    if (permissionsString != null && permissionsString.Trim().StartsWith("["))
                    {
                        var parsedPermissions = JsonSerializer.Deserialize<string[]>(permissionsString, AppJsonSerializerContext.Default.StringArray);
                        if (parsedPermissions != null)
                        {
                            foreach (var perm in parsedPermissions)
                            {
                                claims.Add(new Claim("permission", perm));
                            }
                        }
                    }
                    else
                    {
                        claims.Add(new Claim("permission", permissionsString ?? string.Empty));
                    }
                    keyValuePairs.Remove("permissions");
                }

                // 3. Other claims (sub, exp, etc)
                claims.AddRange(keyValuePairs.Select(kvp => new Claim(kvp.Key, kvp.Value?.ToString() ?? string.Empty)));
            }

            return claims;
        }

        private byte[] ParseBase64WithoutPadding(string base64)
        {
            switch (base64.Length % 4)
            {
                case 2: base64 += "=="; break;
                case 3: base64 += "="; break;
            }
            return Convert.FromBase64String(base64);
        }
    }
}
