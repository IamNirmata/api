import os
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from .schemas import Token, PromptRequest, CompletionResponse
from .vllm_client import VLLMClient
from .models import User

app = FastAPI()

model_id = os.getenv("MODEL_ID")
gpu_count = int(os.getenv("GPU_COUNT", "1"))

vllm_client = VLLMClient(
    model_id=model_id,
    gpu_ids=list(range(gpu_count)),
    max_gpu_mem_mb=80000
)

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate", response_model=CompletionResponse)
async def generate(request: PromptRequest, current_user: User = Depends(get_current_user)):
    result_text = await vllm_client.generate(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    return CompletionResponse(text=result_text)
