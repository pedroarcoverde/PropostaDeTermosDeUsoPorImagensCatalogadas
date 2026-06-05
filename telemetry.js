// Importa o supabase que você configurou no supabaseClient.js
import { supabase } from './supabaseClient.js';

let startTime;
let currentGroup;
const userId = crypto.randomUUID(); 

document.addEventListener("DOMContentLoaded", () => {
    // Agora capturamos o grupo pela URL (ex: termo.html?tipo=A)
    const urlParams = new URLSearchParams(window.location.search);
    currentGroup = urlParams.get('tipo') || 'A';
    startTime = performance.now();
});

// A função precisa ser exportada para ser chamada no HTML
window.registerDecision = async function(accepted) {
    const endTime = performance.now();
    const timeSpentMs = Math.round(endTime - startTime);

    console.log("Enviando telemetria para Supabase...");

    try {
        // Envia direto para a tabela ConsentRecords no Supabase
        const { error } = await supabase
            .from('ConsentRecords')
            .insert([
                {
                    user_id: userId,
                    experimental_group: currentGroup,
                    has_accepted: accepted,
                    latency_milliseconds: timeSpentMs
                }
            ]);

        if (error) throw error;

        alert(`Decisão registrada com sucesso no Supabase!\nTempo de processamento: ${timeSpentMs} ms`);
        window.location.href = `quiz.html?tipo=${currentGroup}&uid=${userId}`;
        
    } catch (error) {
        console.error('Erro ao salvar no Supabase:', error);
        alert('Falha ao registrar consentimento.');
    }
}