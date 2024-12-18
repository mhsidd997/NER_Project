using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using Microsoft.AspNetCore.Cors;

namespace NER_Project.Server.Controllers
{
    [Route("api/[controller]")]
    [EnableCors("AllowSpecificOrigins")] // Apply CORS to this controller
    [ApiController]
    public class NERController : ControllerBase
    {
        [HttpGet]
        public IActionResult Get()
        {
            return Ok("CORS enabled for this endpoint!");
        }

        // Endpoint to process text input
        [HttpPost("process-text")]
        public IActionResult ProcessText([FromBody] TextInput input)
        {
            var result = RunPythonNER(input.Corpus);
            return Ok(result);
        }

        // Endpoint to process PDF file
        [HttpPost("process-pdf")]
        public IActionResult ProcessPdf(IFormFile file)
        {
            if (file == null || file.Length == 0)
                return BadRequest("No file uploaded.");

            // Save PDF temporarily
            var tempFilePath = Path.GetTempFileName();
            using (var stream = new FileStream(tempFilePath, FileMode.Create))
            {
                file.CopyTo(stream);
            }

            // Pass PDF path to Python script
            var result = RunPythonNERForPdf(tempFilePath);

            // Delete temp file
            System.IO.File.Delete(tempFilePath);

            return Ok(result);
        }

        // Helper method to run Python script for text
        private string RunPythonNER(string inputText)
        {
            var psi = new ProcessStartInfo();
            psi.FileName = "python";
            psi.Arguments = $"Scripts/ner_processor.py \"{inputText}\"";
            psi.UseShellExecute = false;
            psi.RedirectStandardOutput = true;

            var process = Process.Start(psi);
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            return output;
        }

        // Helper method to run Python script for PDF
        private string RunPythonNERForPdf(string pdfPath)
        {
            var psi = new ProcessStartInfo();
            psi.FileName = "python";
            psi.Arguments = $"Scripts/ner_processor.py --pdf \"{pdfPath}\"";
            psi.UseShellExecute = false;
            psi.RedirectStandardOutput = true;

            var process = Process.Start(psi);
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            return output;
        }
    }

    public class TextInput
    {
        public string Corpus { get; set; }
    }
}
