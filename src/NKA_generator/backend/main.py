from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from enum import Enum, auto

# ========== Tokeny a Lexer ==========
class TokenType(Enum):
    LCBRA = auto()
    RCBRA = auto()
    LBRACK = auto()
    RBRACK = auto()
    PIPE = auto()
    SYMBOL = auto()
    EPSILON = auto()
    EOF = auto()

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"<{self.type.name},{self.value}>"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        self.pos += 1

    def get_next_token(self):
        while self.pos < len(self.text):
            current = self.peek()
            if current.isspace():
                self.advance()
                continue
            elif current == '{':
                self.advance()
                return Token(TokenType.LCBRA, '{')
            elif current == '}':
                self.advance()
                return Token(TokenType.RCBRA, '}')
            elif current == '[':
                self.advance()
                return Token(TokenType.LBRACK, '[')
            elif current == ']':
                self.advance()
                return Token(TokenType.RBRACK, ']')
            elif current == '|':
                self.advance()
                return Token(TokenType.PIPE, '|')
            elif current == 'ε':
                self.advance()
                return Token(TokenType.EPSILON, 'ε')
            else:
                self.advance()
                return Token(TokenType.SYMBOL, current)
        return Token(TokenType.EOF, None)


class DerivationNode:
    def __init__(self, label):
        self.label = label
        self.children = []

    def add(self, child):
        self.children.append(child)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            val = self.current_token
            self.current_token = self.lexer.get_next_token()
            return val
        else:
            raise Exception(f"Unexpected token {self.current_token}, expected {token_type}")

    def parse(self):
        return self.regular()

    def regular(self):
        print("Parsujem regular")
        node = DerivationNode('regular')
        node.add(self.alternative())
        return node

    def alternative(self):
        node = DerivationNode('alternative')
        left = self.sequence()
        node.add(left)
        while self.current_token.type == TokenType.PIPE:
            pipe_token = self.eat(TokenType.PIPE)
            pipe_node = DerivationNode(f"<{pipe_token.type.name}>")
            node.add(pipe_node)
            right = self.sequence()
            node.add(right)
        return node

    def sequence(self):
        node = DerivationNode('sequence')
        while self.current_token.type in {TokenType.SYMBOL, TokenType.EPSILON, TokenType.LCBRA, TokenType.LBRACK}:
            node.add(self.element())
        return node

    def element(self):
        print(f"Parsujem element pre token {self.current_token}")
        node = DerivationNode('element')
        if self.current_token.type == TokenType.LCBRA:
            lcbra = self.eat(TokenType.LCBRA)
            node.add(DerivationNode(f"<{lcbra.type.name}>"))
            inner = self.regular()
            node.add(inner)
            rcbra = self.eat(TokenType.RCBRA)
            node.add(DerivationNode(f"<{rcbra.type.name}>"))
        elif self.current_token.type == TokenType.SYMBOL:
            symbol = self.eat(TokenType.SYMBOL)
            node.add(DerivationNode(f"<{symbol.type.name},{symbol.value}>"))
        elif self.current_token.type == TokenType.EPSILON:
            epsilon = self.eat(TokenType.EPSILON)
            node.add(DerivationNode(f"<{epsilon.type.name}>"))
        elif self.current_token.type == TokenType.LBRACK:
            lbrack = self.eat(TokenType.LBRACK)
            node.add(DerivationNode(f"<{lbrack.type.name}>"))
            inner = self.regular()
            node.add(inner)
            rbrack = self.eat(TokenType.RBRACK)
            node.add(DerivationNode(f"<{rbrack.type.name}>"))
        else:
            raise Exception(f"Unexpected token in element: {self.current_token}")
        return node


def generate_nka_from_tree(node, state_counter=[0]):
    def new_state():
        state = f"q{state_counter[0]}"
        state_counter[0] += 1
        return state

    def walk(node):
        label = node.label

        if label.startswith("<SYMBOL,"):
            symbol = label.split(",")[1][0]
            start = new_state()
            end = new_state()
            return {
                "states": {start, end},
                "alphabet": {symbol},
                "transitions": {(start, symbol): {end}},
                "start": start,
                "accepts": {end}
            }

        elif label == "sequence":
            nfas = [walk(child) for child in node.children]
            result = nfas[0]
            for next_nfa in nfas[1:]:
                for accept_state in result["accepts"]:
                    result["transitions"].setdefault((accept_state, None), set()).add(next_nfa["start"])
                result["states"].update(next_nfa["states"])
                result["transitions"].update(next_nfa["transitions"])
                result["accepts"] = next_nfa["accepts"]
            return result

        elif label == "alternative":
            nfas = []
            for child in node.children:
                if child.label.startswith("<"):
                    continue  # skip <PIPE>
                nfas.append(walk(child))

            start = new_state()
            end = new_state()
            states = {start, end}
            alphabet = set()
            transitions = {}

            for nfa in nfas:
                transitions.setdefault((start, None), set()).add(nfa["start"])
                for a in nfa["accepts"]:
                    transitions.setdefault((a, None), set()).add(end)
                states.update(nfa["states"])
                alphabet.update(nfa["alphabet"])
                transitions.update(nfa["transitions"])

            return {
                "states": states,
                "alphabet": alphabet,
                "transitions": transitions,
                "start": start,
                "accepts": {end}
            }


        elif label == "element":

            # KLEENE STAR pre {}

            if len(node.children) == 3 and node.children[0].label == "<LCBRA>":

                inner = walk(node.children[1])

                new_start = new_state()

                new_accept = new_state()

                transitions = dict(inner["transitions"])

                transitions.setdefault((new_start, None), set()).add(inner["start"])

                transitions.setdefault((new_start, None), set()).add(new_accept)

                for a in inner["accepts"]:
                    transitions.setdefault((a, None), set()).update({inner["start"], new_accept})

                return {

                    "states": inner["states"].union({new_start, new_accept}),

                    "alphabet": inner["alphabet"],

                    "transitions": transitions,

                    "start": new_start,

                    "accepts": {new_accept}

                }

            # VOLITEĽNOSŤ pre []

            elif len(node.children) == 3 and node.children[0].label == "<LBRACK>":

                # Voliteľnosť [R] == (R | ε)

                inner = walk(node.children[1])

                new_start = new_state()

                new_accept = new_state()

                transitions = dict(inner["transitions"])

                transitions.setdefault((new_start, None), set()).add(inner["start"])

                transitions.setdefault((new_start, None), set()).add(new_accept)

                for a in inner["accepts"]:
                    transitions.setdefault((a, None), set()).add(new_accept)

                return {

                    "states": inner["states"].union({new_start, new_accept}),

                    "alphabet": inner["alphabet"],

                    "transitions": transitions,

                    "start": new_start,

                    "accepts": {new_accept}

                }

            else:

                return walk(node.children[0])

        elif label == "regular":
            return walk(node.children[0])

        return {
            "states": set(),
            "alphabet": set(),
            "transitions": {},
            "start": "",
            "accepts": set()
        }

    return walk(node)



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class RegexRequest(BaseModel):
    regex: str

class SimulateRequest(BaseModel):
    regex: str
    word: str

def derivation_tree_to_json(node):
    return {
        "label": node.label,
        "children": [derivation_tree_to_json(child) for child in node.children]
    }

@app.post("/tree")
def get_derivation_tree(req: RegexRequest):
    lexer = Lexer(req.regex)
    parser = Parser(lexer)
    tree = parser.parse()
    print(json.dumps(derivation_tree_to_json(tree), indent=2))
    return derivation_tree_to_json(tree)

@app.post("/nka")
def get_nka(req: RegexRequest):
    lexer = Lexer(req.regex)
    parser = Parser(lexer)
    tree = parser.parse()
    nka = generate_nka_from_tree(tree)
    nka_json = {
        "states": list(nka["states"]),
        "alphabet": list(nka["alphabet"]),
        "transitions": {str(k): list(v) for k, v in nka["transitions"].items()},
        "start": nka["start"],
        "accepts": list(nka["accepts"])
    }
    return nka_json

@app.post("/simulate")
def simulate_nka_api(req: SimulateRequest):
    lexer = Lexer(req.regex)
    parser = Parser(lexer)
    tree = parser.parse()
    nka = generate_nka_from_tree(tree)
    def simulate_nka(nka, word):
        current_states = set()
        next_states = set()
        def epsilon_closure(states):
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                for (s, sym), targets in nka['transitions'].items():
                    if s == state and sym is None:
                        for t in targets:
                            if t not in closure:
                                closure.add(t)
                                stack.append(t)
            return closure
        current_states = epsilon_closure({nka['start']})
        for symbol in word:
            next_states.clear()
            for state in current_states:
                targets = nka['transitions'].get((state, symbol), set())
                next_states.update(targets)
            current_states = epsilon_closure(next_states)
        return any(s in nka['accepts'] for s in current_states)
    accepted = simulate_nka(nka, req.word)
    return {"accepted": accepted}

# --- Spustenie pre uvicorn: ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
