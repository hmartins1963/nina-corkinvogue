from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os

app = FastAPI(title="Nina Wellness - Cork in Vogue")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConsultaRequest(BaseModel):
    mensagem: str
    area: str = "geral"

NINA_SYSTEM_PROMPT = """
Você é a Nina, assistente de wellness especializada em bem-estar para a comunidade do Cork in Vogue.

SUA PERSONALIDADE:
- Empática e acolhedora
- Linguagem acessível mas profissional  
- Foca em soluções práticas
- Usa emojis moderadamente 🌱

ÁREAS:
🍎 NUTRIÇÃO: Alimentação saudável, receitas práticas
😊 SAÚDE MENTAL: Gestão de stress, mindfulness  
💪 EXERCÍCIO: Atividade física adaptável
🌙 BEM-ESTAR: Sono, rotina, autocuidado

REGRAS:
🚫 NUNCA dê diagnósticos médicos
🚫 NUNCA prescreva medicamentos
✅ SEMPRE encaminhe para profissionais
✅ Priorize a segurança dos usuários
"""

@app.post("/consulta")
async def consultar_nina(consulta: ConsultaRequest):
    try:
        client = anthropic.Anthropic(
            api_key=os.environ['ANTHROPIC_API_KEY']
        )
        
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
            "resposta": "❌ Desculpe, estou com dificuldades técnicas. Tente novamente.",
            "area": consulta.area, 
            "status": "erro"
        }

@app.get("/")
async def home():
    return {"message": "🌱 Nina Wellness API - Cork in Vogue", "status": "online"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
