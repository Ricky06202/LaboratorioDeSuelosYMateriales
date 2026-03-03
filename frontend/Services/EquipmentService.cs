using System.Net.Http.Json;
using System.IO;
using frontend.Models;
using Microsoft.AspNetCore.WebUtilities;

namespace frontend.Services
{
    public class EquipmentService
    {
        private readonly HttpClient _httpClient;

        public EquipmentService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<EquipoResponse> GetEquiposAsync(int skip = 0, int limit = 10, string? search = null)
        {
            var query = new Dictionary<string, string>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            if (!string.IsNullOrEmpty(search)) query["search"] = search;

            var url = QueryHelpers.AddQueryString("api/equipos/", query);
            return await _httpClient.GetFromJsonAsync<EquipoResponse>(url);
        }

        public async Task<List<Equipo>> GetAlertsAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<Equipo>>("api/equipos/alerts/calibrations") ?? new();
        }

        public async Task<Equipo> GetEquipoAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<Equipo>($"api/equipos/{id}") ?? throw new Exception("Equipo no encontrado");
        }

        public async Task<Equipo> CreateEquipoAsync(EquipoCreate equipo)
        {
            var response = await _httpClient.PostAsJsonAsync("api/equipos/", equipo);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Equipo>() ?? throw new Exception("Error al crear equipo");
        }

        public async Task<Equipo> UpdateEquipoAsync(Guid id, EquipoUpdate equipo)
        {
            var response = await _httpClient.PutAsJsonAsync($"api/equipos/{id}", equipo);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Equipo>() ?? throw new Exception("Error al actualizar equipo");
        }

        public async Task DeleteEquipoAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/equipos/{id}");
            response.EnsureSuccessStatusCode();
        }

        public async Task<string> UploadPhotoAsync(Guid id, Stream fileStream, string fileName)
        {
            using var content = new MultipartFormDataContent();
            var fileContent = new StreamContent(fileStream);
            content.Add(fileContent, "file", fileName);

            var response = await _httpClient.PostAsync($"api/equipos/{id}/foto", content);
            response.EnsureSuccessStatusCode();
            var result = await response.Content.ReadFromJsonAsync<UploadResult>();
            return result?.Filename ?? throw new Exception("Error al subir foto");
        }

        public async Task<Calibracion> CreateCalibracionAsync(CalibracionCreate calibracion, Stream? fileStream = null, string? fileName = null)
        {
            // For simplicity in the initial implementation, we'll send the metadata first
            // and then handle the file if present. In a more robust implementation,
            // we'd use multipart for the whole request or separate endpoints.
            // Current backend expect JSON metadata and optional file in separate parts for certifications
            // but the C# PostAsJsonAsync doesn't support mixing easily.
            // Let's use multipart if file exists.
            
            if (fileStream != null && fileName != null)
            {
                using var content = new MultipartFormDataContent();
                // Add JSON parts manually or as string parts
                content.Add(new StringContent(calibracion.EquipoId.ToString()), "equipo_id");
                content.Add(new StringContent(calibracion.FechaCalibracion.ToString("yyyy-MM-dd")), "fecha_calibracion");
                content.Add(new StringContent(calibracion.FechaVencimiento.ToString("yyyy-MM-dd")), "fecha_vencimiento");
                content.Add(new StringContent(calibracion.EmpresaCertificadora), "empresa_certificadora");
                
                var fileContent = new StreamContent(fileStream);
                content.Add(fileContent, "file", fileName);

                var response = await _httpClient.PostAsync("api/equipos/calibrations", content);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadFromJsonAsync<Calibracion>() ?? throw new Exception("Error al crear calibración");
            }
            else
            {
                var response = await _httpClient.PostAsJsonAsync("api/equipos/calibrations", calibracion);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadFromJsonAsync<Calibracion>() ?? throw new Exception("Error al crear calibración");
            }
        }

        private class UploadResult { public string Filename { get; set; } = ""; }
    }
}
