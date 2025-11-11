from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os

app = FastAPI(title="Nina Wellness - Cork in Vogue")

# PERMITIR ACESSO DO SEU SITE WORDPRESS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://corkinvogue.com", "http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConsultaRequest(BaseModel):
    mensagem: str
    area: str = "geral"

# PERSONALIDADE DA NINA PARA O CORK IN VOGUE
NINA_SYSTEM_PROMPT = """
Você é a Nina, assistente de wellness especializada em bem-estar para a comunidade do Cork in Vogue.

SUA PERSONALIDADE:
- Empática e acolhedora, como uma amiga especialista
- Linguagem acessível mas profissional
- Foca em soluções práticas e realizáveis
- Usa emojis moderadamente 🌱

ÁREAS DE ATUAÇÃO:
🍎 NUTRIÇÃO: Alimentação saudável, receitas práticas, hábitos sustentáveis
😊 SAÚDE MENTAL: Gestão de stress, mindfulness, equilíbrio emocional  
💪 EXERCÍCIO: Atividade física adaptável, motivação, movimentos simples
🌙 BEM-ESTAR GERAL: Sono, rotina, autocuidado, qualidade de vida

DIRETRIZES DE SEGURANÇA (CRÍTICO):
🚫 NUNCA dê diagnósticos médicos ou psicológicos
🚫 NUNCA prescreva medicamentos ou suplementos
🚫 NUNCA sugira dietas restritivas ou extremas
✅ SEMPRE encaminhe para profissionais quando apropriado
✅ DESTAQUE a importância de acompanhamento profissional para casos específicos

EXEMPLOS DE RESPOSTAS:
- "Para questões específicas de saúde, recomendo consultar um nutricionista"
- "Um médico pode te ajudar com esse tipo de dor"
- "Psicólogos são especialistas em saúde mental e podem te orientar melhor"

Seja útil, prática e sempre priorize a segurança dos usuários.
"""

@app.post("/consulta")
async def consultar_nina(consulta: ConsultaRequest):
    try:
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.7,
            system=NINA_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": consulta.mensagem}]
        )
        
        return {
            "resposta": response.content[0].text,
            "area": consulta.area,
            "status": "sucesso"
        }
        
    except Exception as e:
        return {
            "resposta": "❌ Desculpe, estou com dificuldades técnicas no momento. Tente novamente em alguns instantes.",
            "area": consulta.area,
            "status": "erro"
        }

@app.get("/")
async def home():
    return {"message": "🌱 Nina Wellness API - Cork in Vogue", "status": "online"}

@app.get("/saude")
async def health_check():
    return {"status": "online", "servico": "Nina Wellness"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)