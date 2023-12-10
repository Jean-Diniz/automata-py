import uvicorn
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/dfa")
async def automata(request: Request):
    info = await request.json()
    final_states, initial_state, input_symbols, input_w, states, transitions = getJsonData(info)

    dfa = DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    if dfa.read_input(input_w):
        return {"message": "Aceita"}
    else:
        return {"message": "Rejeita"}


@app.post("/dpda")
async def automata(request: Request):
    info = await request.json()
    final_states, initial_state, input_symbols, input_w, states, transitions = getJsonData(info)

    initial_stack_symbol = info.get("initial_stack_symbol", "")
    if initial_stack_symbol == "":
        raise HTTPException(status_code=400, detail="Estado inicial da stack não pode ser vazio")

    stack_symbols = set(info.get("stack_symbols", []))
    if len(stack_symbols) == 0:
        raise HTTPException(status_code=400, detail="Stack simbolos não pode ser vazio")

    dpda = DPDA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        stack_symbols=stack_symbols,
        initial_stack_symbol=initial_stack_symbol,
        final_states=final_states,
        acceptance_mode='final_state'
    )

    if dpda.accepts_input(input_w):
        return {"message": "Aceita"}
    else:
        return {"message": "Rejeita"}


@app.post("/nfa")
async def automata(request: Request):
    info = await request.json()
    final_states, initial_state, input_symbols, input_w, states, transitions = getJsonData(info)

    nfa = NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    if nfa.accepts_input(input_w):
        return {"message": "Aceita"}
    else:
        return {"message": "Rejeita"}


def getJsonData(json):
    states = set(json.get("states", []))
    if len(states) == 0:
        raise HTTPException(status_code=400, detail="Estado não pode ser vazio")
    input_symbols = set(json.get("input_symbols", []))
    if len(input_symbols) == 0:
        raise HTTPException(status_code=400, detail="Simbolos não pode ser vazio")
    transitions = dict(json.get("transitions", {}))
    if len(transitions) == 0:
        raise HTTPException(status_code=400, detail="Transições não pode ser vazio")
    initial_state = json.get("initial_state", "")
    if initial_state == "":
        raise HTTPException(status_code=400, detail="Estado inicial não pode ser vazio")
    final_states = set(json.get("final_states", ""))
    if len(final_states) == 0:
        raise HTTPException(status_code=400, detail="Estados finais não pode ser vazio")
    input_w = json.get("input_w", "")
    if input_w == "":
        raise HTTPException(status_code=400, detail="Input não pode ser vazio")
    return final_states, initial_state, input_symbols, input_w, states, transitions


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
