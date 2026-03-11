using System.Text.Json.Serialization;

namespace frontend.Models
{
    public class ApiError
    {
        [JsonPropertyName("detail")]
        public string Detail { get; set; } = string.Empty;
    }

    public class UploadResult
    {
        [JsonPropertyName("filename")]
        public string Filename { get; set; } = string.Empty;
    }

    public class TokenResponse
    {
        [JsonPropertyName("access_token")]
        public string AccessToken { get; set; } = string.Empty;

        [JsonPropertyName("token_type")]
        public string TokenType { get; set; } = string.Empty;
    }
}
