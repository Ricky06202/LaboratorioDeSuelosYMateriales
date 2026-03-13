using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using frontend.Models;

namespace frontend.Services
{
    public static class HttpResponseHelper
    {
        public static async Task EnsureSuccessOrThrowAsync(HttpResponseMessage response)
        {
            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                
                string errorMessage;
                
                if (response.StatusCode == HttpStatusCode.Unauthorized)
                {
                    errorMessage = "Su sesión ha expirado. Por favor, cierre sesión y vuelva a iniciar.";
                }
                else if (response.StatusCode == HttpStatusCode.Forbidden)
                {
                    errorMessage = "No tiene permisos para realizar esta acción. Contacte al administrador del sistema.";
                }
                else if (response.StatusCode == HttpStatusCode.NotFound)
                {
                    errorMessage = "El registro solicitado no fue encontrado en la base de datos.";
                }
                else if (response.StatusCode == HttpStatusCode.BadRequest)
                {
                    try
                    {
                        var error = JsonSerializer.Deserialize<ApiError>(content);
                        if (error != null && !string.IsNullOrEmpty(error.Detail))
                        {
                            throw new Exception(error.Detail);
                        }
                    }
                    catch { }
                    errorMessage = "Los datos enviados no son válidos. Por favor, verifique la información ingresada.";
                }
                else if (response.StatusCode == HttpStatusCode.Conflict)
                {
                    errorMessage = "Ya existe un registro con estos datos. Por favor, verifique.";
                }
                else if (response.StatusCode == HttpStatusCode.UnprocessableEntity)
                {
                    try
                    {
                        var error = JsonSerializer.Deserialize<ApiError>(content);
                        if (error != null && !string.IsNullOrEmpty(error.Detail))
                        {
                            throw new Exception(error.Detail);
                        }
                    }
                    catch { }
                    errorMessage = "Error de validación. Por favor, revise los datos e intente nuevamente.";
                }
                else
                {
                    try
                    {
                        var error = JsonSerializer.Deserialize<ApiError>(content);
                        if (error != null && !string.IsNullOrEmpty(error.Detail))
                        {
                            throw new Exception(error.Detail);
                        }
                    }
                    catch { }
                    errorMessage = $"Error del servidor ({response.StatusCode}). Por favor, intente más tarde o contacte soporte técnico.";
                }
                
                throw new Exception(errorMessage);
            }
        }
    }
}
