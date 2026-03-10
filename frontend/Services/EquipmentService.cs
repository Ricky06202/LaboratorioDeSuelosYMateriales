using System.Net.Http.Json;
using System.IO;
using frontend.Models;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.JSInterop;
using System.Net.Http.Headers;
namespace frontend.Services
{
    public class EquipmentService
    {
        private readonly HttpClient _httpClient;
        private readonly IJSRuntime _jsRuntime;

        public EquipmentService(HttpClient httpClient, IJSRuntime jsRuntime)
        {
            _httpClient = httpClient;
            _jsRuntime = jsRuntime;
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

            if (!string.IsNullOrEmpty(equipo.TipoFondo))
                content.Add(new StringContent(equipo.TipoFondo), "tipo_fondo");

            if (!string.IsNullOrEmpty(equipo.OrdenCompra))
                content.Add(new StringContent(equipo.OrdenCompra), "orden_compra");

            if (!string.IsNullOrEmpty(equipo.SolicitudNo))
                content.Add(new StringContent(equipo.SolicitudNo), "solicitud_no");

            if (!string.IsNullOrEmpty(equipo.TipoBien))
                content.Add(new StringContent(equipo.TipoBien), "tipo_bien");

            if (equipo.FechaRecibido.HasValue)
                content.Add(new StringContent(equipo.FechaRecibido.Value.ToString("yyyy-MM-dd")), "fecha_recibido");

            if (!string.IsNullOrEmpty(equipo.IdAsignado))
                content.Add(new StringContent(equipo.IdAsignado), "id_asignado");

            if (!string.IsNullOrEmpty(equipo.Capacidad))
                content.Add(new StringContent(equipo.Capacidad), "capacidad");

            if (!string.IsNullOrEmpty(equipo.UbicacionFisica))
                content.Add(new StringContent(equipo.UbicacionFisica), "ubicacion_fisica");

            if (!string.IsNullOrEmpty(equipo.Proveedor))
                content.Add(new StringContent(equipo.Proveedor), "proveedor");

            if (!string.IsNullOrEmpty(equipo.EstadoAprobacion))
                content.Add(new StringContent(equipo.EstadoAprobacion), "estado_aprobacion");

            if (!string.IsNullOrEmpty(equipo.Observations))
                content.Add(new StringContent(equipo.Observations), "observaciones");

            if (!string.IsNullOrEmpty(equipo.VerificadoPor))
                content.Add(new StringContent(equipo.VerificadoPor), "verificado_por");

            if (!string.IsNullOrEmpty(equipo.RevisadoPor))
                content.Add(new StringContent(equipo.RevisadoPor), "revisado_por");

            if (equipo.FechaVerificacion.HasValue)
                content.Add(new StringContent(equipo.FechaVerificacion.Value.ToString("yyyy-MM-dd")), "fecha_verificacion");

            if (equipo.FechaRevision.HasValue)
                content.Add(new StringContent(equipo.FechaRevision.Value.ToString("yyyy-MM-dd")), "fecha_revision");

            if (!string.IsNullOrEmpty(equipo.RangoCalibracion))
                content.Add(new StringContent(equipo.RangoCalibracion), "rango_calibracion");

            if (equipo.FrecuenciaCalibracion.HasValue)
                content.Add(new StringContent(equipo.FrecuenciaCalibracion.Value.ToString()), "frecuencia_calibracion");

            if (!string.IsNullOrEmpty(equipo.MetodoMantenimiento))
                content.Add(new StringContent(equipo.MetodoMantenimiento), "metodo_mantenimiento");

            // Add Criteria
            content.Add(new StringContent(equipo.Criteria1.ToString().ToLower()), "criteria_1");
            content.Add(new StringContent(equipo.Criteria2.ToString().ToLower()), "criteria_2");
            content.Add(new StringContent(equipo.Criteria3.ToString().ToLower()), "criteria_3");
            content.Add(new StringContent(equipo.Criteria4.ToString().ToLower()), "criteria_4");
            content.Add(new StringContent(equipo.Criteria5.ToString().ToLower()), "criteria_5");
            content.Add(new StringContent(equipo.Criteria6.ToString().ToLower()), "criteria_6");
            content.Add(new StringContent(equipo.Criteria7.ToString().ToLower()), "criteria_7");
            content.Add(new StringContent(equipo.Criteria8.ToString().ToLower()), "criteria_8");
            content.Add(new StringContent(equipo.Criteria9.ToString().ToLower()), "criteria_9");
            content.Add(new StringContent(equipo.Criteria10.ToString().ToLower()), "criteria_10");
            content.Add(new StringContent(equipo.Criteria11.ToString().ToLower()), "criteria_11");
            content.Add(new StringContent(equipo.Criteria12.ToString().ToLower()), "criteria_12");
            content.Add(new StringContent(equipo.Criteria13.ToString().ToLower()), "criteria_13");
            content.Add(new StringContent(equipo.Criteria14.ToString().ToLower()), "criteria_14");

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

        public async Task<byte[]> GetReportPdfAsync(string endpoint)
        {
            var response = await _httpClient.GetAsync(endpoint);
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadAsByteArrayAsync();
        }

        public async Task<Stream> DownloadEquipmentReportAsync(Guid equipoId, string type)
        {
            await SetAuthorizationHeaderAsync();
            var response = await _httpClient.GetAsync($"api/equipos/{equipoId}/reports/{type}");
            await EnsureSuccessOrThrowAsync(response);
            return await response.Content.ReadAsStreamAsync();
        }

        private async Task SetAuthorizationHeaderAsync()
        {
            var token = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", "authToken");
            if (!string.IsNullOrWhiteSpace(token))
            {
                _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            }
        }
        private async Task EnsureSuccessOrThrowAsync(HttpResponseMessage response)
        {
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                try
                {
                    // Try to parse as the "Error Hunter" format first
                    using var doc = System.Text.Json.JsonDocument.Parse(content);
                    if (doc.RootElement.TryGetProperty("error", out var errorProp))
                    {
                        throw new Exception(errorProp.GetString());
                    }
                    if (doc.RootElement.TryGetProperty("detail", out var detailProp))
                    {
                        if (detailProp.ValueKind == System.Text.Json.JsonValueKind.String)
                            throw new Exception(detailProp.GetString());
                        else
                            throw new Exception("Error de validación en el servidor.");
                    }
                }
                catch (Exception ex) when (ex is not Exception) { } // Ignore JSON parsing errors only
                
                throw new Exception($"Error {response.StatusCode}: {content}");
            }
        }

        private class ApiError { public string Detail { get; set; } = ""; }
        private class UploadResult { public string Filename { get; set; } = ""; }
    }
}
