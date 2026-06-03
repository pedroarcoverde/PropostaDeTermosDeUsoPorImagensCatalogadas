using Microsoft.AspNetCore.Mvc;
using ConsentTelemetry.Interfaces;
using ConsentTelemetry.Models;

namespace ConsentTelemetry.Controllers;

public class HomeController : Controller
{
    private readonly IConsentRepository _consentRepository;

    public HomeController(IConsentRepository consentRepository)
    {
        _consentRepository = consentRepository;
    }

    public IActionResult Index()
    {
        return View();
    }

    public IActionResult TermosDeUso(string tipo)
    {
        var variant = string.Equals(tipo, "B", StringComparison.OrdinalIgnoreCase) ? "B" : "A";

        var model = new TermosDeUsoViewModel
        {
            Variant = variant,
            Title = variant == "B" ? "Termo de Uso - Variante B" : "Termo de Uso - Variante A",
            ContentHtml = variant == "B"
                ? "<p>Este termo apresenta o uso estendido de dados e a visualização mais transparente do ciclo de tratamento.</p><ul><li>Dados de sessão são usados para atender à experiência.</li><li>Compartilhamento de metadados com parceiros é permitido.</li><li>Você pode revogar o consentimento a qualquer momento.</li></ul>"
                : "<p>Este termo apresenta a versão padrão de compromisso, com foco em clareza mínima e linguagem direta.</p><ul><li>Coleta de dados estritamente necessária para o serviço.</li><li>Nenhum compartilhamento adicional é feito sem autorização.</li><li>Processo de exclusão disponível mediante solicitação.</li></ul>"
        };

        return View(model);
    }

    public async Task<IActionResult> Logs()
    {
        var logs = await _consentRepository.GetAllAsync();
        return View(logs);
    }
}
