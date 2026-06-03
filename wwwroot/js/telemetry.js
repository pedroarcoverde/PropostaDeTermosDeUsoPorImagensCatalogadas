// Variáveis de controle de sessão
let startTime;
let currentGroup;
const userId = crypto.randomUUID(); // Identificador anônimo para a sessão

// Inicialização do fluxo de termo de uso
document.addEventListener("DOMContentLoaded", () => {
    currentGroup = window.termVariant || 'A';
    startTime = performance.now();
});

// Captura a decisão e envia métricas para o Back-end
async function registerDecision(accepted) {
    const endTime = performance.now();
    const timeSpentMs = Math.round(endTime - startTime);

    const payload = {
        UserId: userId,
        Group: currentGroup,
        Accepted: accepted,
        TimeSpentMilliseconds: timeSpentMs,
        Timestamp: new Date().toISOString()
    };

    console.log("Enviando telemetria:", payload);

    try {
        const response = await fetch(`${window.location.origin}/api/consent/log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert(`Decisão registrada com sucesso.\nTempo de processamento: ${timeSpentMs} ms`);
            window.location.href = '/';
        } else {
            console.error('Falha ao registrar consentimento.');
        }
    } catch (error) {
        console.error('Erro de rede na comunicação com o backend:', error);
    }
}
