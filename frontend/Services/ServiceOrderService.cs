using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.AspNetCore.WebUtilities;

namespace frontend.Services
{
    public class ServiceOrderService
    {
        private readonly HttpClient _httpClient;

        public ServiceOrderService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<ServiceOrder>> GetServiceOrdersAsync(int skip = 0, int limit = 100)
        {
            var query = new Dictionary<string, string?>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            var url = QueryHelpers.AddQueryString("api/ordenes-servicio/", query);
            return await _httpClient.GetFromJsonAsync<List<ServiceOrder>>(url, AppJsonSerializerContext.Default.ListServiceOrder) ?? new List<ServiceOrder>();
        }

        public async Task<ServiceOrder> GetServiceOrderAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<ServiceOrder>($"api/ordenes-servicio/{id}", AppJsonSerializerContext.Default.ServiceOrder) 
                   ?? throw new Exception("Orden de servicio no encontrada");
        }

        public async Task<ServiceOrder> CreateServiceOrderAsync(ServiceOrderCreate serviceOrder)
        {
            var response = await _httpClient.PostAsJsonAsync("api/ordenes-servicio/", serviceOrder, AppJsonSerializerContext.Default.ServiceOrderCreate);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<ServiceOrder>(AppJsonSerializerContext.Default.ServiceOrder) 
                   ?? throw new Exception("Error al crear la orden de servicio");
        }

        public async Task DeleteServiceOrderAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/ordenes-servicio/{id}");
            await EnsureSuccessOrThrowAsync(response);
        }

        public async Task<byte[]> GetServiceOrderPdfAsync(Guid id)
        {
            var response = await _httpClient.GetAsync($"api/ordenes-servicio/{id}/pdf");
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadAsByteArrayAsync();
        }

        private async Task EnsureSuccessOrThrowAsync(HttpResponseMessage response)
        {
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                try
                {
                    var error = System.Text.Json.JsonSerializer.Deserialize<ApiError>(content, AppJsonSerializerContext.Default.ApiError);
                    if (error != null && !string.IsNullOrEmpty(error.Detail))
                    {
                        throw new Exception(error.Detail);
                    }
                }
                catch { } // Fallback
                
                throw new Exception($"Error {response.StatusCode}: No se pudo completar la operación.");
            }
        }
    }
}
