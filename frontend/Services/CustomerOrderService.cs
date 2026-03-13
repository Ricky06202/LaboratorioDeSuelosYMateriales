using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.AspNetCore.WebUtilities;

namespace frontend.Services
{
    public class CustomerOrderService
    {
        private readonly HttpClient _httpClient;

        public CustomerOrderService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<CustomerOrder>> GetCustomerOrdersAsync(int skip = 0, int limit = 100)
        {
            var query = new Dictionary<string, string?>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            var url = QueryHelpers.AddQueryString("api/pedidos/", query);
            return await _httpClient.GetFromJsonAsync<List<CustomerOrder>>(url, AppJsonSerializerContext.Default.ListCustomerOrder) ?? new List<CustomerOrder>();
        }

        public async Task<CustomerOrder> GetCustomerOrderAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<CustomerOrder>($"api/pedidos/{id}", AppJsonSerializerContext.Default.CustomerOrder) 
                   ?? throw new Exception("Pedido no encontrado");
        }

        public async Task<CustomerOrder> CreateCustomerOrderAsync(CustomerOrderCreate order)
        {
            var response = await _httpClient.PostAsJsonAsync("api/pedidos/", order, AppJsonSerializerContext.Default.CustomerOrderCreate);
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<CustomerOrder>(AppJsonSerializerContext.Default.CustomerOrder) 
                   ?? throw new Exception("Error al crear el pedido. No se recibió respuesta del servidor.");
        }

        public async Task UpdateCustomerOrderAsync(Guid id, CustomerOrderCreate order)
        {
            var response = await _httpClient.PutAsJsonAsync($"api/pedidos/{id}", order, AppJsonSerializerContext.Default.CustomerOrderCreate);
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
        }

        public async Task DeleteCustomerOrderAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/pedidos/{id}");
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
        }

        public async Task<byte[]> GetCustomerOrderPdfAsync(Guid id)
        {
            var response = await _httpClient.GetAsync($"api/pedidos/{id}/pdf");
            await HttpResponseHelper.EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadAsByteArrayAsync();
        }
    }
}
