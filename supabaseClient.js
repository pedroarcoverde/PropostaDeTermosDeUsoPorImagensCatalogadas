// Importa o Supabase via CDN
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const supabaseUrl = 'https://pkljcjsdlndkxnybavpk.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrbGpjanNkbG5ka3hueWJhdnBrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA2Nzg2MTYsImV4cCI6MjA5NjI1NDYxNn0.5osjRhXsKLEezjWbGFpeU2-hSEmUw3kP3jS9NSeqV_w';


export const supabase = createClient(supabaseUrl, supabaseKey);