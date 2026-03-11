using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using frontend.Models;
using Microsoft.JSInterop;

namespace frontend.Services
{
    public class CalendarService
    {
        private readonly HttpClient _httpClient;
        private readonly IJSRuntime _jsRuntime;

        public CalendarService(HttpClient httpClient, IJSRuntime jsRuntime)
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

        public async Task<List<CalendarActivity>> GetActivitiesAsync(DateTime? start = null, DateTime? end = null)
        {
            await SetAuthorizationHeaderAsync();
            var url = "/api/agenda/";
            var queryParams = new List<string>();
            if (start.HasValue) queryParams.Add($"start={start.Value:yyyy-MM-ddTHH:mm:ss}");
            if (end.HasValue) queryParams.Add($"end={end.Value:yyyy-MM-ddTHH:mm:ss}");
            
            if (queryParams.Count > 0) url += "?" + string.Join("&", queryParams);
            
            return await _httpClient.GetFromJsonAsync<List<CalendarActivity>>(url, AppJsonSerializerContext.Default.ListCalendarActivity) ?? new();
        }

        public async Task<CalendarActivity> CreateActivityAsync(CalendarActivityCreate activity)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PostAsJsonAsync("/api/agenda/", activity, AppJsonSerializerContext.Default.CalendarActivityCreate);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<CalendarActivity>(AppJsonSerializerContext.Default.CalendarActivity))!;
        }

        public async Task<CalendarActivity> UpdateActivityAsync(Guid id, CalendarActivityCreate activity) // Reusing Create for Update properties
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.PutAsJsonAsync($"/api/agenda/{id}", activity, AppJsonSerializerContext.Default.CalendarActivityCreate);
            response.EnsureSuccessStatusCode();
            return (await response.Content.ReadFromJsonAsync<CalendarActivity>(AppJsonSerializerContext.Default.CalendarActivity))!;
        }

        public async Task DeleteActivityAsync(Guid id)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.DeleteAsync($"/api/agenda/{id}");
            response.EnsureSuccessStatusCode();
        }
    }
}
