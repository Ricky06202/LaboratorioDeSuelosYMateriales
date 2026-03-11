using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.JSInterop;

namespace frontend.Services
{
    public class LabServiceService
    {
        private readonly HttpClient _httpClient;
        private readonly IJSRuntime _jsRuntime;

        public LabServiceService(HttpClient httpClient, IJSRuntime jsRuntime)
        {
            _httpClient = httpClient;
            _jsRuntime = jsRuntime;
        }

        private async Task SetAuthorizationHeaderAsync()
        {
            var token = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", "authToken");
            if (!string.IsNullOrEmpty(token))
            {
                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
            }
        }

        public async Task<List<LabService>> GetServicesAsync(string? search = null)
        {
            await SetAuthorizationHeaderAsync();
            var url = "/api/servicios/";
            if (!string.IsNullOrWhiteSpace(search)) url += $"?search={search}";
            return await _httpClient.GetFromJsonAsync<List<LabService>>(url) ?? new();
        }

        public async Task<LabService?> GetServiceAsync(int id)
        {
            await SetAuthorizationHeaderAsync();
            return await _httpClient.GetFromJsonAsync<LabService>($"/api/servicios/{id}");
        }

        public async Task<LabService> CreateServiceAsync(LabServiceCreate service)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PostAsJsonAsync("/api/servicios/", service);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<LabService>())!;
        }

        public async Task<LabService> UpdateServiceAsync(int id, LabServiceUpdate service)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PutAsJsonAsync($"/api/servicios/{id}", service);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<LabService>())!;
        }

        public async Task DeleteServiceAsync(int id)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.DeleteAsync($"/api/servicios/{id}");
            response.EnsureSuccessStatusCode();
        }
    }
}
