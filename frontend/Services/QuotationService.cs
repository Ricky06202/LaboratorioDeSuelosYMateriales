using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.AspNetCore.WebUtilities;

namespace frontend.Services
{
    public class QuotationService
    {
        private readonly HttpClient _httpClient;

        public QuotationService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<Quotation>> GetQuotationsAsync(int skip = 0, int limit = 100)
        {
            var query = new Dictionary<string, string>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            var url = QueryHelpers.AddQueryString("api/cotizaciones/", query);
            return await _httpClient.GetFromJsonAsync<List<Quotation>>(url) ?? new List<Quotation>();
        }

        public async Task<Quotation> GetQuotationAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<Quotation>($"api/cotizaciones/{id}") 
                   ?? throw new Exception("Cotización no encontrada");
        }

        public async Task<Quotation> CreateQuotationAsync(QuotationCreate quotation)
        {
            var response = await _httpClient.PostAsJsonAsync("api/cotizaciones/", quotation);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Quotation>() 
                   ?? throw new Exception("Error al crear la cotización");
        }

        public async Task DeleteQuotationAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/cotizaciones/{id}");
            await EnsureSuccessOrThrowAsync(response);
        }

        public async Task<byte[]> GetQuotationPdfAsync(Guid id)
        {
            var response = await _httpClient.GetAsync($"api/cotizaciones/{id}/pdf");
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
                    var error = System.Text.Json.JsonSerializer.Deserialize<ApiError>(content, new System.Text.Json.JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                    if (error != null && !string.IsNullOrEmpty(error.Detail))
                    {
                        throw new Exception(error.Detail);
                    }
                }
                catch { } // Fallback
                
                throw new Exception($"Error {response.StatusCode}: No se pudo completar la operación.");
            }
        }

        private class ApiError { public string Detail { get; set; } = ""; }
    }
}
