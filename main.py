import json
import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from llama_index import (
    VectorStoreIndex,
    ServiceContext
)
from llama_index.chat_engine.types import BaseChatEngine
from llama_index.llms import OpenAI
from pydantic import BaseModel
from qdrant_client.http.exceptions import UnexpectedResponse

logging.basicConfig(stream=sys.stdout, level="DEBUG")

app = FastAPI()

@app.get("/query")
async def query(temperature: float = 0.0,
                model: str = "gpt-3.5-turbo"):
    query = "Who is George Washington?"
    logging.info(f"Query: {query}")
    service_context = ServiceContext.from_defaults(llm=OpenAI(model=model,
                                                              temperature=temperature))

    index = VectorStoreIndex.from_documents([],
                                            service_context = service_context)
    
    async def _generate_streaming_response(chat_engine: BaseChatEngine,
                                           query: str):
        response = await chat_engine.astream_chat(message=query)
    
        for token in response.response_gen:
            logging.debug(f"Token: {token}")
            yield json.dumps(token)[1:-1]

    try:
        chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
        return StreamingResponse(
            _generate_streaming_response(chat_engine=chat_engine,
                                         query=query)
                                 )
    except UnexpectedResponse as e:
        raise HTTPException(status_code=404, detail=str(e))
