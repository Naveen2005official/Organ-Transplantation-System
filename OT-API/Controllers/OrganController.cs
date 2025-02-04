using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Text;

namespace OT_API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class OrganController : ControllerBase
    {
        private readonly HttpClient _httpClient;

        public OrganController(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        [HttpPost("match")]
        public async Task<IActionResult> GetBestDonor([FromBody] RecipientDto recipient)
        {
            var flaskUrl = "http://127.0.0.1:5000/predict";  // Flask API URL

            var jsonContent = new StringContent(JsonConvert.SerializeObject(recipient), Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync(flaskUrl, jsonContent);

            if (!response.IsSuccessStatusCode)
            {
                return BadRequest("Error calling Flask API");
            }

            var bestDonor = await response.Content.ReadAsStringAsync();
            return Ok(bestDonor);
        }
    }

    // DTO class for recipient
    public class RecipientDto
    {
        public int Recipient_Age { get; set; }
        public string Recipient_Gender { get; set; }
        public string Recipient_Blood_Type { get; set; }
        public string Organ_Type_Needed { get; set; }
        public int Priority_Level { get; set; }
        public int Wait_Time_Months { get; set; }
    }
}
