from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os

app = FastAPI()

# Configuração CORS - permite todos os domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConsultaRequest(BaseModel):
    mensagem: str
    area: str = "geral"

NINA_PROMPT = """
Você é a Nina, assistente de wellness especializada em bem-estar.
Seja empática, útil e baseada em ciência.
Nunca dê conselhos médicos - sempre encaminhe para profissionais.
"""

@app.post("/consulta")
async def consultar_nina(consulta: ConsultaRequest):
    try:
        client = anthropic.Anthropic(
            api_key=os.environ['ANTHROPIC_API_KEY']
        )
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0.7,
            system=NINA_PROMPT,
            messages=[{"role": "user", "content": consulta.mensagem}]
        )
        
        return {
            "resposta": response.content[0].text,
            "area": consulta.area
        }
        
    except Exception as e:
        return {
            "resposta": "Desculpe, estou com dificuldades técnicas. Tente novamente.",
            "area": consulta.area
        }

@app.get("/")
async def home():
    return {"message": "Nina Wellness API - Online"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
