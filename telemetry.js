window.startTime = performance.now();
const urlParams = new URLSearchParams(window.location.search);
window.currentGroup = urlParams.get('tipo') || 'A';
window.userId = crypto.randomUUID();

window.registerDecision = function(accepted) {
    const timeSpentMs = Math.round(performance.now() - window.startTime);
    
    // Salva os dados temporariamente no navegador
    sessionStorage.setItem('temp_consent', JSON.stringify({
        user_id: window.userId,
        experimental_group: window.currentGroup,
        has_accepted: accepted,
        latency_milliseconds: timeSpentMs
    }));

    // Vai para o quiz
    window.location.href = 'quiz.html';
};