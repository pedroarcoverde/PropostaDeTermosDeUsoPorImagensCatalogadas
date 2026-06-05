// Importa o Supabase via CDN (ideal para projetos estáticos HTML/JS puro)
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const supabaseUrl = 'HTTPS://SEU-PROJETO.supabase.co';
const supabaseKey = 'SUA_CHAVE_ANON_PUBLICA';

export const supabase = createClient(supabaseUrl, supabaseKey);