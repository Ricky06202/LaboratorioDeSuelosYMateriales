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

        public async Task<List<Quotation>> GetQuotationsAsync(int skip = 0, int limit = 100, Guid? customerOrderId = null)
        {
            var query = new Dictionary<string, string?>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            if (customerOrderId.HasValue)
            {
                query["customer_order_id"] = customerOrderId.Value.ToString();
            }
            var url = QueryHelpers.AddQueryString("api/cotizaciones/", query);
            return await _httpClient.GetFromJsonAsync<List<Quotation>>(url, AppJsonSerializerContext.Default.ListQuotation) ?? new List<Quotation>();
        }

        public async Task<Quotation> GetQuotationAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<Quotation>($"api/cotizaciones/{id}", AppJsonSerializerContext.Default.Quotation) 
                   ?? throw new Exception("Cotización no encontrada");
        }

        public async Task<Quotation> CreateQuotationAsync(QuotationCreate quotation)
        {
            var response = await _httpClient.PostAsJsonAsync("api/cotizaciones/", quotation, AppJsonSerializerContext.Default.QuotationCreate);
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Quotation>(AppJsonSerializerContext.Default.Quotation) 
                   ?? throw new Exception("Error al crear la cotización. No se recibió respuesta del servidor.");
        }

        public async Task DeleteQuotationAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/cotizaciones/{id}");
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
        }

        public async Task<byte[]> GetQuotationPdfAsync(Guid id)
        {
            var response = await _httpClient.GetAsync($"api/cotizaciones/{id}/pdf");
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadAsByteArrayAsync();
        }
    }
}
