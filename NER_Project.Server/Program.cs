var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Add CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigins", policy =>
    {
        policy.WithOrigins("https://example.com", "http://localhost:3000") // Add allowed origins
              .AllowAnyHeader() // Allow specific headers (or use .WithHeaders("header-name"))
              .AllowAnyMethod(); // Allow specific HTTP methods (or use .WithMethods("GET", "POST"))
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
app.UseRouting();

// Use the CORS middleware
app.UseCors("AllowSpecificOrigins");

app.UseAuthorization();

app.MapControllers();

app.Run();
