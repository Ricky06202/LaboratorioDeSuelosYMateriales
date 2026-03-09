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

        public async Task<EquipoResponse> GetEquiposAsync(int skip = 0, int limit = 10, string? search = null, string? estado = null)
        {
            var query = new Dictionary<string, string?>
            {
                ["skip"] = skip.ToString(),
                ["limit"] = limit.ToString()
            };
            if (!string.IsNullOrEmpty(search)) query["search"] = search;
            if (!string.IsNullOrEmpty(estado)) query["estado"] = estado;


            var url = QueryHelpers.AddQueryString("api/equipos/", query);
            return await _httpClient.GetFromJsonAsync<EquipoResponse>(url) ?? new EquipoResponse();
        }

        public async Task<List<Equipo>> GetAlertsAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<Equipo>>("api/equipos/alerts/calibrations") ?? new();
        }

        public async Task<Equipo> GetEquipoAsync(Guid id)
        {
            return await _httpClient.GetFromJsonAsync<Equipo>($"api/equipos/{id}") ?? throw new Exception("Equipo no encontrado");
        }

        public async Task<Equipo> CreateEquipoAsync(EquipoCreate equipo, Stream? fileStream = null, string? fileName = null)
        {
            using var content = new MultipartFormDataContent();
            content.Add(new StringContent(equipo.Nombre ?? ""), "nombre");
            content.Add(new StringContent(equipo.NumeroSerie ?? ""), "numero_serie");
            content.Add(new StringContent(equipo.Estado ?? "Activo"), "estado");
            
            if (!string.IsNullOrEmpty(equipo.Marca))
                content.Add(new StringContent(equipo.Marca), "marca");
                
            if (!string.IsNullOrEmpty(equipo.Modelo))
                content.Add(new StringContent(equipo.Modelo), "modelo");

            // Assuming Ubicacion might be added to EquipoCreate in C# later if needed
            
            if (fileStream != null && !string.IsNullOrEmpty(fileName))
            {
                var fileContent = new StreamContent(fileStream);
                content.Add(fileContent, "file", fileName);
            }

            var response = await _httpClient.PostAsync("api/equipos/", content);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Equipo>() ?? throw new Exception("Error al crear equipo");
        }

        public async Task<Equipo> UpdateEquipoAsync(Guid id, EquipoUpdate equipo)
        {
            var response = await _httpClient.PutAsJsonAsync($"api/equipos/{id}", equipo);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Equipo>() ?? throw new Exception("Error al actualizar equipo");
        }

        public async Task DeleteEquipoAsync(Guid id)
        {
            var response = await _httpClient.DeleteAsync($"api/equipos/{id}");
            await EnsureSuccessOrThrowAsync(response);
        }

        public async Task<string> UploadPhotoAsync(Guid id, Stream fileStream, string fileName)
        {
            using var content = new MultipartFormDataContent();
            var fileContent = new StreamContent(fileStream);
            content.Add(fileContent, "file", fileName);

            var response = await _httpClient.PostAsync($"api/equipos/{id}/foto", content);
            await EnsureSuccessOrThrowAsync(response);
            var result = await response.Content.ReadFromJsonAsync<UploadResult>();
            return result?.Filename ?? throw new Exception("Error al subir foto");
        }

        public async Task<Calibracion> CreateCalibracionAsync(CalibracionCreate calibracion, Stream? fileStream = null, string? fileName = null)
        {
            using var content = new MultipartFormDataContent();
            content.Add(new StringContent(calibracion.EquipoId.ToString()), "equipo_id");
            content.Add(new StringContent(calibracion.FechaCalibracion.ToString("yyyy-MM-dd")), "fecha_calibracion");
            content.Add(new StringContent(calibracion.FechaVencimiento.ToString("yyyy-MM-dd")), "fecha_vencimiento");
            content.Add(new StringContent(calibracion.EmpresaCertificadora ?? ""), "empresa_certificadora");
            
            if (fileStream != null && !string.IsNullOrEmpty(fileName))
            {
                var fileContent = new StreamContent(fileStream);
                content.Add(fileContent, "file", fileName);
            }

            var response = await _httpClient.PostAsync("api/equipos/calibrations", content);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadFromJsonAsync<Calibracion>() ?? throw new Exception("Error al crear calibración");
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
                catch { } // Fallback if parsing fails
                
                throw new Exception($"Error {response.StatusCode}: No se pudo completar la operación.");
            }
        }

        private class ApiError { public string Detail { get; set; } = ""; }
        private class UploadResult { public string Filename { get; set; } = ""; }
    }
}
