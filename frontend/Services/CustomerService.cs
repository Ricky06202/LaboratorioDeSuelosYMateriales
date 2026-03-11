using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.JSInterop;

namespace frontend.Services
{
    public class CustomerService
    {
        private readonly HttpClient _httpClient;
        private readonly IJSRuntime _jsRuntime;

        public CustomerService(HttpClient httpClient, IJSRuntime jsRuntime)
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

        public async Task<List<Customer>> GetCustomersAsync(string? search = null)
        {
            await SetAuthorizationHeaderAsync();
            var url = "/api/clientes/";
            if (!string.IsNullOrWhiteSpace(search)) url += $"?search={search}";
            return await _httpClient.GetFromJsonAsync<List<Customer>>(url, AppJsonSerializerContext.Default.ListCustomer) ?? new();
        }

        public async Task<Customer?> GetCustomerAsync(Guid id)
        {
            await SetAuthorizationHeaderAsync();
            return await _httpClient.GetFromJsonAsync<Customer>($"/api/clientes/{id}", AppJsonSerializerContext.Default.Customer);
        }

        public async Task<Customer> CreateCustomerAsync(CustomerCreate customer)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PostAsJsonAsync("/api/clientes/", customer, AppJsonSerializerContext.Default.CustomerCreate);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<Customer>(AppJsonSerializerContext.Default.Customer))!;
        }

        public async Task<Customer> UpdateCustomerAsync(Guid id, CustomerUpdate customer)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PutAsJsonAsync($"/api/clientes/{id}", customer, AppJsonSerializerContext.Default.CustomerUpdate);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<Customer>(AppJsonSerializerContext.Default.Customer))!;
        }

        public async Task DeleteCustomerAsync(Guid id)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.DeleteAsync($"/api/clientes/{id}");
            response.EnsureSuccessStatusCode();
        }
    }
}
