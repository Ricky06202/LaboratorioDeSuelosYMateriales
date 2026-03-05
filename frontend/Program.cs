using frontend.Auth;
using frontend.Components;
using frontend.Services;
using Microsoft.AspNetCore.Components.Authorization;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddAuthorization();
builder.Services.AddScoped<AuthenticationStateProvider, JwtAuthenticationStateProvider>();
builder.Services.AddCascadingAuthenticationState();
builder.Services.AddMudServices();
builder.Services.AddHttpClient<EquipmentService>(client => {
    client.BaseAddress = new Uri("http://localhost:8000/");
    client.Timeout = TimeSpan.FromSeconds(10);
});
builder.Services.AddHttpClient<QuotationService>(client => {
    client.BaseAddress = new Uri("http://localhost:8000/");
    client.Timeout = TimeSpan.FromSeconds(10);
});
builder.Services.AddHttpClient<ServiceOrderService>(client => {
    client.BaseAddress = new Uri("http://localhost:8000/");
    client.Timeout = TimeSpan.FromSeconds(10);
});
builder.Services.AddHttpClient<CustomerOrderService>(client => {
    client.BaseAddress = new Uri("http://localhost:8000/");
    client.Timeout = TimeSpan.FromSeconds(10);
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}
app.UseStatusCodePagesWithReExecute("/not-found", createScopeForStatusCodePages: true);
app.UseHttpsRedirection();

app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
